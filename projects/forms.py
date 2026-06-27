from django import forms
from .models import Client, Project, Task, TimeLog, Invoice, InvoiceItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'company', 'address']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client', 'title', 'description', 'status', 'hourly_rate',
                  'fixed_price', 'start_date', 'deadline']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['start_time', 'end_time', 'note']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['project', 'invoice_number', 'issue_date', 'due_date', 'status', 'notes']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


InvoiceItemFormSet = forms.inlineformset_factory(
    Invoice, InvoiceItem, fields=['description', 'quantity', 'rate'], extra=1, can_delete=True
)