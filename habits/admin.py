from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change) -> None:
        obj.full_clean()
        super().save_model(request, obj, form, change)
