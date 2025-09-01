from django.urls import path

from .views import HabitDetailView, PublicHabitListView, UserHabitListCreateView

urlpatterns = [
    path("my/", UserHabitListCreateView.as_view(), name="my-habits"),
    path("public/", PublicHabitListView.as_view(), name="public-habits"),
    path("<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
]
