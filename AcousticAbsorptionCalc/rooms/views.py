from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Room
from .forms import RoomForm


class RoomListView(ListView):
    model = Room
    template_name = "rooms/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        return Room.objects.filter(project__id=self.kwargs.get('project_id'))


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"

    def form_valid(self, form):
        form.instance.project_id = self.kwargs.get("project_id") 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("rooms:room_list", kwargs={"project_id": self.kwargs.get("project_id")})

