from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks.views import ProjectViewSet, RegisterView, TaskViewSet, UserViewSet


router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("tasks", TaskViewSet, basename="task")
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
]
