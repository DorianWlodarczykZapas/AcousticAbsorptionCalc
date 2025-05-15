from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from project_logs.projectlogger import ProjectLogger
from user_logs.logger import Logger

from .forms import FurnishingFormSet, RoomForm
from .models import Room


class RoomListView(ListView):
    model = Room
    template_name = "rooms/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.filter(project__id=self.kwargs.get("project_id"))


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["furnishing_formset"] = FurnishingFormSet(self.request.POST)
        else:
            context["furnishing_formset"] = FurnishingFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["furnishing_formset"]

        if formset.is_valid():
            form.instance.project_id = self.kwargs.get("project_id")
            response = super().form_valid(form)

            furnishings = {
                f.cleaned_data["material"].name: f.cleaned_data["area"]
                for f in formset
                if f.cleaned_data and not f.cleaned_data.get("DELETE", False)
            }

            Logger.log_room_created(
                user_id=self.object.pk, changed_by=self.request.user
            )

            ProjectLogger.log_room_created(
                project=self.object.project,
                changed_by=self.request.user,
                change_description=f"Room '{form.cleaned_data['name']}' created",
                metadata=furnishings,
            )

            print("Furnishing data:", furnishings)

            return response
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "rooms:room_list", kwargs={"project_id": self.kwargs.get("project_id")}
        )


class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"
    context_object_name = "room"

    def form_valid(self, form):
        response = super().form_valid(form)

        Logger.log_room_updated(user_id=self.object.pk, changed_by=self.request.user)

        return response

    def get_success_url(self):
        return reverse_lazy(
            "rooms:room_list", kwargs={"project_id": self.object.project_id}
        )


class ProjectRoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/project_room_form.html"
    context_object_name = "room"

    def form_valid(self, form):
        old_name = self.object.name
        old_area = self.object.area

        response = super().form_valid(form)

        Logger.log_room_updated(user_id=self.object.pk, changed_by=self.request.user)

        ProjectLogger.log_edit_furnishing(
            project=self.object.project,
            changed_by=self.request.user,
            change_description=f"Room '{old_name}' updated in project.",
            metadata={
                "room_id": self.object.pk,
                "old_name": old_name,
                "new_name": self.object.name,
                "old_area": old_area,
                "new_area": self.object.area,
            },
        )

        return response

    def get_success_url(self):
        return reverse_lazy(
            "rooms:room_list", kwargs={"project_id": self.object.project_id}
        )


class RoomDeleteView(DeleteView):
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
