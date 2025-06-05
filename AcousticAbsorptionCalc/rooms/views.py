from calculations.acoustic_calculator import AcousticCalculator
from calculations.models import Calculation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView
from project_logs.projectlogger import ProjectLogger
from user_logs.logger import Logger

from .forms import FurnishingFormSet, MoveRoomForm, RoomForm
from .models import Furnishing, Room, RoomMaterial


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
        else:
            context["furnishing_formset"] = FurnishingFormSet(prefix="furnishing")

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["furnishing_formset"]

        if formset.is_valid():
            form.instance.project_id = self.kwargs.get("project_id")
            response = super().form_valid(form)

            construction_mapping = {
                "floor": form.cleaned_data.get("floor_material"),
                "ceiling": form.cleaned_data.get("ceiling_material"),
                "wall A": form.cleaned_data.get("wall_a_material"),
                "wall B": form.cleaned_data.get("wall_b_material"),
                "wall C": form.cleaned_data.get("wall_c_material"),
                "wall D": form.cleaned_data.get("wall_d_material"),
            }

            construction_data = []
            for location, material in construction_mapping.items():
                if material:
                    RoomMaterial.objects.create(
                        room=self.object,
                        material=material,
                        location=location,
                    )
                    area = self._estimate_surface_area(self.object, location)
                    construction_data.append(
                        {
                            "material": material,
                            "area_m2": area,
                        }
                    )

            furnishing_data = []
            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get("DELETE", False):
                    Furnishing.objects.create(
                        room=self.object,
                        name=f.cleaned_data["material"].name,
                        material=f.cleaned_data["material"],
                        quantity=1,
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

    @staticmethod
    def _estimate_surface_area(room, location: str) -> float:
        width = float(room.width)
        length = float(room.length)
        height = float(room.height)

        if location in ["wall A", "wall C"]:
            return height * length
        elif location in ["wall B", "wall D"]:
            return height * width
        elif location in ["floor", "ceiling"]:
            return width * length
        return 0.0


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
        else:
            furnishings = Furnishing.objects.filter(room=self.object)
            initial_data = [
                {"material": f.material, "area": f.quantity} for f in furnishings
            ]
            context["furnishing_formset"] = FurnishingFormSet(
                initial=initial_data, prefix="furnishing"
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["furnishing_formset"]

        if not formset.is_valid():
            return self.form_invalid(form)

        response = super().form_valid(form)

        RoomMaterial.objects.filter(room=self.object).delete()
        construction_mapping = {
            "floor": form.cleaned_data.get("floor_material"),
            "ceiling": form.cleaned_data.get("ceiling_material"),
            "wall A": form.cleaned_data.get("wall_a_material"),
            "wall B": form.cleaned_data.get("wall_b_material"),
            "wall C": form.cleaned_data.get("wall_c_material"),
            "wall D": form.cleaned_data.get("wall_d_material"),
        }
        for location, material in construction_mapping.items():
            if material:
                RoomMaterial.objects.create(
                    room=self.object, material=material, location=location
                )

        Furnishing.objects.filter(room=self.object).delete()
        for f in formset:
            if f.cleaned_data and not f.cleaned_data.get("DELETE", False):
                Furnishing.objects.create(
                    room=self.object,
                    name=f.cleaned_data["material"].name,
                    material=f.cleaned_data["material"],
                    quantity=1,
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


class MoveRoomView(LoginRequiredMixin, FormView):
    template_name = "rooms/move_room.html"
    form_class = MoveRoomForm

    def dispatch(self, request, *args, **kwargs):
        self.room = Room.objects.get(pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        old_project = self.room.project
        new_project = form.cleaned_data["target_project"]
        if new_project == old_project:
            form.add_error("target_project", "Room is already in this project.")
            return self.form_invalid(form)

        self.room.project = new_project
        self.room.save()

        ProjectLogger.log_edit_furnishing(
            project=new_project,
            changed_by=self.request.user,
            change_description=f"Room '{self.room.name}' moved from project '{old_project.name}'",
            metadata={
                "room_id": self.room.pk,
                "from_project": old_project.pk,
                "to_project": new_project.pk,
            },
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "rooms:room_list", kwargs={"project_id": self.room.project.pk}
        )
