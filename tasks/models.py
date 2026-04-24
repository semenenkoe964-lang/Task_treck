from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_projects",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="projects",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    deadline = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_tasks",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("deadline", "-created_at")

    def __str__(self):
        return self.title
