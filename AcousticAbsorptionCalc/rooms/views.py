from calculations.models import Calculation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import FurnishingFormSet, RoomForm, RoomSurfaceFormSet
from .models import Furnishing, Room, RoomSurface


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "rooms/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.select_related("project").prefetch_related("furnishings")


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["surface_formset"] = RoomSurfaceFormSet(
                self.request.POST, prefix="surface"
            )
            context["furnishing_formset"] = FurnishingFormSet(
                self.request.POST, prefix="furnishing"
            )
        else:
            context["surface_formset"] = RoomSurfaceFormSet(prefix="surface")
            context["furnishing_formset"] = FurnishingFormSet(prefix="furnishing")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        surface_formset = context["surface_formset"]
        furnishing_formset = context["furnishing_formset"]

        if surface_formset.is_valid() and furnishing_formset.is_valid():
            self.object = form.save()

            # Save surfaces
            for surface_form in surface_formset:
                if surface_form.cleaned_data and not surface_form.cleaned_data.get(
                    "DELETE", False
                ):
                    surface = surface_form.save(commit=False)
                    surface.room = self.object
                    surface.save()

            # Save furnishings
            for furnishing_form in furnishing_formset:
                if (
                    furnishing_form.cleaned_data
                    and not furnishing_form.cleaned_data.get("DELETE", False)
                ):
                    Furnishing.objects.create(
                        room=self.object,
                        material=furnishing_form.cleaned_data["material"],
                        quantity=furnishing_form.cleaned_data["quantity"],
                    )

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("rooms:room_list")


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"
    context_object_name = "room"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["surface_formset"] = RoomSurfaceFormSet(
                self.request.POST, prefix="surface"
            )
            context["furnishing_formset"] = FurnishingFormSet(
                self.request.POST, prefix="furnishing"
            )
        else:
            surfaces = RoomSurface.objects.filter(room=self.object)
            context["surface_formset"] = RoomSurfaceFormSet(
                queryset=surfaces, prefix="surface"
            )

            furnishings = Furnishing.objects.filter(room=self.object)
            initial_furnishings = [
                {"material": f.material, "quantity": f.quantity} for f in furnishings
            ]
            context["furnishing_formset"] = FurnishingFormSet(
                initial=initial_furnishings, prefix="furnishing"
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        surface_formset = context["surface_formset"]
        furnishing_formset = context["furnishing_formset"]

        if surface_formset.is_valid() and furnishing_formset.is_valid():
            response = super().form_valid(form)

            # Clear old data
            RoomSurface.objects.filter(room=self.object).delete()
            Furnishing.objects.filter(room=self.object).delete()

            # Save new surfaces
            for surface_form in surface_formset:
                if surface_form.cleaned_data and not surface_form.cleaned_data.get(
                    "DELETE", False
                ):
                    surface = surface_form.save(commit=False)
                    surface.room = self.object
                    surface.save()

            # Save new furnishings
            for furnishing_form in furnishing_formset:
                if (
                    furnishing_form.cleaned_data
                    and not furnishing_form.cleaned_data.get("DELETE", False)
                ):
                    Furnishing.objects.create(
                        room=self.object,
                        material=furnishing_form.cleaned_data["material"],
                        quantity=furnishing_form.cleaned_data["quantity"],
                    )

            return response
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("rooms:room_list")


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = "rooms/room_delete.html"
    context_object_name = "room"

    def get_success_url(self):
        return reverse_lazy("rooms:room_list")


class RoomCalculationSummaryView(DetailView):
    model = Room
    template_name = "rooms/room_summary.html"
    context_object_name = "room"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("surfaces", "furnishings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["calculation"] = self.object.calculation
        except Calculation.DoesNotExist:
            context["calculation"] = None
        return context
