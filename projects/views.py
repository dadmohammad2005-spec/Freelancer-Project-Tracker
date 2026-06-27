from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Client, Project, Task, TimeLog, Invoice
from .forms import (ClientForm, ProjectForm, TaskForm, TimeLogForm,
                     InvoiceForm, InvoiceItemFormSet)
from .forms import RegisterForm

# ---------- DASHBOARD ----------
@login_required
def dashboard(request):
    context = {
        'total_clients': Client.objects.count(),
        'total_projects': Project.objects.count(),
        'active_projects': Project.objects.filter(status='active').count(),
        'pending_tasks': Task.objects.exclude(status='done').count(),
        'unpaid_invoices': Invoice.objects.exclude(status='paid').count(),
        'recent_projects': Project.objects.all()[:5],
    }
    return render(request, 'projects/dashboard.html', context)


# ---------- CLIENTS ----------
@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'projects/client_list.html', {'clients': clients})


@login_required
def client_create(request):
    form = ClientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Client added successfully.")
        return redirect('client_list')
    return render(request, 'projects/client_form.html', {'form': form})


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Client updated successfully.")
        return redirect('client_list')
    return render(request, 'projects/client_form.html', {'form': form})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, "Client deleted.")
        return redirect('client_list')
    return render(request, 'projects/confirm_delete.html', {'object': client})


# ---------- PROJECTS ----------
@login_required
def project_list(request):
    projects = Project.objects.select_related('client').all()
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Project created successfully.")
        return redirect('project_list')
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Project updated successfully.")
        return redirect('project_detail', pk=pk)
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted.")
        return redirect('project_list')
    return render(request, 'projects/confirm_delete.html', {'object': project})


# ---------- TASKS ----------
@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()
        messages.success(request, "Task added.")
        return redirect('project_detail', pk=project_pk)
    return render(request, 'projects/task_form.html', {'form': form, 'project': project})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Task updated.")
        return redirect('project_detail', pk=task.project.pk)
    return render(request, 'projects/task_form.html', {'form': form, 'project': task.project})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted.")
        return redirect('project_detail', pk=project_pk)
    return render(request, 'projects/confirm_delete.html', {'object': task})


# ---------- TIME TRACKING ----------
@login_required
def timelog_create(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    form = TimeLogForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        log = form.save(commit=False)
        log.task = task
        log.save()
        messages.success(request, "Time log added.")
        return redirect('project_detail', pk=task.project.pk)
    return render(request, 'projects/timelog_form.html', {'form': form, 'task': task})


@login_required
def timelog_delete(request, pk):
    log = get_object_or_404(TimeLog, pk=pk)
    project_pk = log.task.project.pk
    if request.method == 'POST':
        log.delete()
        return redirect('project_detail', pk=project_pk)
    return render(request, 'projects/confirm_delete.html', {'object': log})


# ---------- INVOICES ----------
@login_required
def invoice_list(request):
    invoices = Invoice.objects.select_related('project', 'project__client').all()
    return render(request, 'projects/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'projects/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_create(request):
    form = InvoiceForm(request.POST or None)
    formset = InvoiceItemFormSet(request.POST or None)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        invoice = form.save()
        formset.instance = invoice
        formset.save()
        messages.success(request, "Invoice created.")
        return redirect('invoice_detail', pk=invoice.pk)
    return render(request, 'projects/invoice_form.html', {'form': form, 'formset': formset})


@login_required
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    form = InvoiceForm(request.POST or None, instance=invoice)
    formset = InvoiceItemFormSet(request.POST or None, instance=invoice)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        messages.success(request, "Invoice updated.")
        return redirect('invoice_detail', pk=pk)
    return render(request, 'projects/invoice_form.html', {'form': form, 'formset': formset})


@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'projects/confirm_delete.html', {'object': invoice})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})