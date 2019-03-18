from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, FormView

from projects.models import Project, Task
from projects.templatetags.project_extras import get_accepted_task_offer
from .forms import PaymentForm
from .models import Payment


def payment(request, project_id, task_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id)
    sender = project.user
    receiver = get_accepted_task_offer(task).offerer

    if request.method == 'POST':
        Payment.objects.create(payer=sender, receiver=receiver, task=task)
        task.status = Task.PAYMENT_SENT
        task.save()

        return redirect('receipt', project_id=project_id, task_id=task_id)

    return render(request, 'payment/payment.html', {'form': PaymentForm()})


class ReceiptView(TemplateView):
    template_name = "payment/receipt.html"

    def get_context_data(self, project_id, task_id, **kwargs):
        context_data = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=task_id)
        project = get_object_or_404(Project, pk=project_id)
        context_data.update({
            "project": project,
            "task": task,
            "taskoffer": get_accepted_task_offer(task),
        })
        return context_data
