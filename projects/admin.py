from django.contrib import admin
from .models import Client, Project, Task, TimeLog, Invoice, InvoiceItem


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'created_at')
    search_fields = ('name', 'email', 'company')


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'status', 'hourly_rate', 'start_date', 'deadline')
    list_filter = ('status',)
    search_fields = ('title', 'client__name')
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'assigned_to', 'due_date')
    list_filter = ('status', 'project')


@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'start_time', 'end_time', 'duration_hours')


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'project', 'status', 'issue_date', 'due_date', 'total_amount')
    list_filter = ('status',)
    inlines = [InvoiceItemInline]