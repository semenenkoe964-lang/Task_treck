from django.contrib import admin

from tasks.models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "creator", "created_at")
    search_fields = ("name", "creator__username")
    filter_horizontal = ("members",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "status", "priority", "author", "assignee", "deadline")
    list_filter = ("status", "priority", "project")
    search_fields = ("title", "project__name", "author__username", "assignee__username")
