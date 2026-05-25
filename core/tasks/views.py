from .models import Tasks

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class TaskListView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user)
