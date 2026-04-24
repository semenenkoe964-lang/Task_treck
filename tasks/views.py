from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets

from tasks.filters import TaskFilter
from tasks.models import Project, Task
from tasks.permissions import ProjectPermission, TaskPermission
from tasks.serializers import ProjectSerializer, RegisterSerializer, TaskSerializer, UserSerializer


@extend_schema(tags=["Authentication"])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []


@extend_schema(tags=["Users"])
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(projects__members=self.request.user).distinct().order_by("username")


@extend_schema(tags=["Projects"])
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def get_queryset(self):
        return (
            Project.objects.filter(members=self.request.user)
            .select_related("creator")
            .prefetch_related("members")
            .distinct()
        )


@extend_schema(tags=["Tasks"])
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]
    filterset_class = TaskFilter
    ordering_fields = ("deadline", "created_at", "priority", "status")

    def get_queryset(self):
        return (
            Task.objects.filter(project__members=self.request.user)
            .select_related("project", "author", "assignee", "project__creator")
            .distinct()
        )
