from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Project, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name", "last_name", "email")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "creator", "members", "created_at")
        read_only_fields = ("id", "creator", "created_at")

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        project = Project.objects.create(creator=self.context["request"].user, **validated_data)
        project.members.add(self.context["request"].user, *members)
        return project

    def update(self, instance, validated_data):
        members = validated_data.pop("members", None)
        instance = super().update(instance, validated_data)
        if members is not None:
            instance.members.set(members)
            instance.members.add(instance.creator)
        return instance


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "project",
            "title",
            "description",
            "priority",
            "status",
            "deadline",
            "author",
            "assignee",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "author", "created_at", "updated_at")

    def validate(self, attrs):
        request = self.context["request"]
        project = attrs.get("project") or getattr(self.instance, "project", None)
        assignee = attrs.get("assignee") or getattr(self.instance, "assignee", None)

        if project and not project.members.filter(id=request.user.id).exists():
            raise serializers.ValidationError("Вы не являетесь участником этого проекта.")

        if project and assignee and not project.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError("Исполнитель должен быть участником проекта.")

        if self.instance:
            self._validate_update_permissions(attrs, request.user)

        return attrs

    def _validate_update_permissions(self, attrs, user):
        if self.instance.project.creator_id == user.id:
            return

        changed_fields = {
            field_name
            for field_name, value in attrs.items()
            if getattr(self.instance, field_name) != value
        }

        allowed_fields = set()
        if self.instance.assignee_id == user.id:
            allowed_fields.update({"status", "priority"})
        if self.instance.author_id == user.id:
            allowed_fields.update({"description"})

        if changed_fields and not changed_fields.issubset(allowed_fields):
            raise serializers.ValidationError("У вас нет прав изменять эти поля задачи.")

    def create(self, validated_data):
        return Task.objects.create(author=self.context["request"].user, **validated_data)
