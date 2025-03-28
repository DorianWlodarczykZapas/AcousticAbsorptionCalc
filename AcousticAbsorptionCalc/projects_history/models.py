from django.db import models
from users.models import User


class ChangeLog(models.Model):
    entity_type = models.CharField(max_length=100)  # CHOICE FIELD
    entity_id = models.IntegerField()  # OUT
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=50)  # CHOICE FIELD
    timestamp = models.DateTimeField(auto_now_add=True)
