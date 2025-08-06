from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_to',
        help_text="Можно указывать только для полезных привычек"
    )
    reward = models.CharField(max_length=255, blank=True, null=True)
    periodicity = models.PositiveIntegerField(default=1, help_text="В днях")
    execution_time = models.PositiveIntegerField(help_text="В секундах")
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.action} в {self.time} ({'приятная' if self.is_pleasant else 'полезная'})"
