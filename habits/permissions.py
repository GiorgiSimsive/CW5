from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from habits.models import Habit


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет редактировать объект только его владельцу.
    """

    def has_object_permission(self, request: Request, view: View, obj: Habit) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj.user == request.user)
