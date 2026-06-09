from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        labels = {
            'title': 'Название',
            'description': 'Описание',
        }
        help_texts = {
            'title': 'Кратко, до 100 символов',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Подробности задачи…'}),
        }