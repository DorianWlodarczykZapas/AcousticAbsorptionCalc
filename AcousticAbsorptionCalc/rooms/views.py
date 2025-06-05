from calculations.acoustic_calculator import AcousticCalculator
from calculations.models import Calculation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from project_logs.projectlogger import ProjectLogger
from user_logs.logger import Logger

from .forms import FurnishingFormSet, RoomForm, RoomSurfaceFormSet
from .models import Furnishing, Room, RoomSurface


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "rooms/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.select_related("project").all()


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["furnishing_formset"] = FurnishingFormSet(
                self.request.POST, prefix="furnishing"
            )
            context["surface_formset"] = RoomSurfaceFormSet(
                self.request.POST, prefix="surface"
            )
        else:
            context["furnishing_formset"] = FurnishingFormSet(prefix="furnishing")
            context["surface_formset"] = RoomSurfaceFormSet(prefix="surface")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        furnishing_formset = context["furnishing_formset"]
        surface_formset = context["surface_formset"]

        if furnishing_formset.is_valid() and surface_formset.is_valid():
            form.instance.project_id = self.kwargs.get("project_id")
            response = super().form_valid(form)

            construction_data = []
            for surface_form in surface_formset:
                if surface_form.cleaned_data and not surface_form.cleaned_data.get(
                    "DELETE", False
                ):
                    surface = surface_form.save(commit=False)
                    surface.room = self.object
                    surface.save()
                    construction_data.append(
                        {
                            "material": surface.material,
                            "area_m2": surface.area,
                        }
                    )

            furnishing_data = []
            for f in furnishing_formset:
                if f.cleaned_data and not f.cleaned_data.get("DELETE", False):
                    Furnishing.objects.create(
                        room=self.object,
                        name=f.cleaned_data["material"].name,
                        material=f.cleaned_data["material"],
                        quantity=f.cleaned_data["area"],
                    )
                    furnishing_data.append(
                        {
                            "material": f.cleaned_data["material"],
                            "area_m2": f.cleaned_data["area"],
                        }
                    )

            norm = self.object.norm
            calculator = AcousticCalculator(
                norm=norm,
                room_dimensions={
                    "height": float(self.object.height),
                    "length": float(self.object.length),
                    "width": float(self.object.width),
                },
                construction_surfaces=construction_data,
                furnishing_elements=furnishing_data,
                freq_band="500",
            )

            validation_result = calculator.validate_surface_match()

            if not validation_result["valid"]:
                print(
                    "[WARNING] Provided construction surface area does not match geometry: "
                    f"expected={validation_result['expected_area']} m², "
                    f"provided={validation_result['provided_area']} m², "
                    f"difference={validation_result['difference']} m²"
                )

            rt = calculator.calculate_rt()
            sti = round(0.75 - rt * 0.2, 2)
            is_within = calculator.is_within_norm(rt)

            Calculation.objects.create(
                norm=norm,
                room_height=self.object.height,
                room_volume=calculator.room_volume,
                room_surface_area=calculator.room_surface_area,
                reverberation_time=rt,
                sti=sti,
                required_absorption=calculator.calculate_required_absorption(),
                achieved_absorption=calculator.calculate_absorption(),
                is_within_norm=is_within,
            )

            Logger.log_room_created(
                user_id=self.object.pk, changed_by=self.request.user
            )
            ProjectLogger.log_room_created(
                project=self.object.project,
                changed_by=self.request.user,
                change_description=("Room '{name}' created").format(
                    name=form.cleaned_data["name"]
                ),
                metadata={f["material"].name: f["area_m2"] for f in furnishing_data},
            )

            return response
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "rooms:room_list", kwargs={"project_id": self.kwargs.get("project_id")}
        )


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"
    context_object_name = "room"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["furnishing_formset"] = FurnishingFormSet(
                self.request.POST, prefix="furnishing"
            )
            context["surface_formset"] = RoomSurfaceFormSet(
                self.request.POST, prefix="surface"
            )
        else:
            furnishings = Furnishing.objects.filter(room=self.object)
            initial_furnishings = [
                {"material": f.material, "area": f.quantity} for f in furnishings
            ]
            context["furnishing_formset"] = FurnishingFormSet(
                initial=initial_furnishings, prefix="furnishing"
            )

            surfaces = RoomSurface.objects.filter(room=self.object)
            context["surface_formset"] = RoomSurfaceFormSet(
                queryset=surfaces, prefix="surface"
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        furnishing_formset = context["furnishing_formset"]
        surface_formset = context["surface_formset"]

        if not (furnishing_formset.is_valid() and surface_formset.is_valid()):
            return self.form_invalid(form)

        response = super().form_valid(form)

        RoomSurface.objects.filter(room=self.object).delete()
        for surface_form in surface_formset:
            if surface_form.cleaned_data and not surface_form.cleaned_data.get(
                "DELETE", False
            ):
                surface = surface_form.save(commit=False)
                surface.room = self.object
                surface.save()

        Furnishing.objects.filter(room=self.object).delete()
        for f in furnishing_formset:
            if f.cleaned_data and not f.cleaned_data.get("DELETE", False):
                Furnishing.objects.create(
                    room=self.object,
                    name=f.cleaned_data["material"].name,
                    material=f.cleaned_data["material"],
                    quantity=f.cleaned_data["area"],
                )

        Logger.log_room_updated(user_id=self.object.pk, changed_by=self.request.user)
        return response

    def get_success_url(self):
        return reverse_lazy(
            "rooms:room_list", kwargs={"project_id": self.object.project_id}
        )


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = "rooms/room_confirm_delete.html"
    context_object_name = "room"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        Logger.log_room_deleted(user_id=self.object.pk, changed_by=request.user)

        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "rooms:room_list", kwargs={"project_id": self.object.project_id}
        )
