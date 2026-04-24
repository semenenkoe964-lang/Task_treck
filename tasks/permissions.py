from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.members.filter(id=request.user.id).exists()
        return obj.creator_id == request.user.id


class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.project.members.filter(id=request.user.id).exists()

        if obj.project.creator_id == request.user.id:
            return True

        if request.method == "DELETE":
            return obj.author_id == request.user.id

        return request.user.id in {obj.author_id, obj.assignee_id}
