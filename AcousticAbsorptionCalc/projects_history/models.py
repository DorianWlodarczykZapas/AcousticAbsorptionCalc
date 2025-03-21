from django.db import models
from users.models import User


class ChangeLog(models.Model):
    entity_type = models.CharField(max_length=100)
    entity_id = models.IntegerField()
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
