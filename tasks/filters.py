import django_filters

from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    deadline_after = django_filters.DateFilter(field_name="deadline", lookup_expr="gte")
    deadline_before = django_filters.DateFilter(field_name="deadline", lookup_expr="lte")

    class Meta:
        model = Task
        fields = {
            "project": ["exact"],
            "status": ["exact"],
            "priority": ["exact"],
            "assignee": ["exact"],
            "deadline": ["exact"],
        }
