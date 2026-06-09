from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from .forms import TaskForm
from django.urls import reverse
from datetime import date, timedelta
from django.utils import timezone
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
@login_required
def task_list(request: HttpRequest) -> HttpResponse:
    '''Показывает задачи текущего юзера за выбранный день'''
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = date.fromisoformat(date_str)
        except ValueError:
            selected_date = timezone.localdate()
    else:
        selected_date = timezone.localdate()

    tasks = Task.objects.filter(user=request.user, date=selected_date)

    context = {
        'tasks': tasks,
        'selected_date': selected_date,
        'prev_date': selected_date - timedelta(days=1),
        'next_date': selected_date + timedelta(days=1),
        'today': timezone.localdate(),
    }
    return render(request, 'tasks/task_list.html', context)


@require_http_methods(["GET", "POST"])
@login_required
def task_create(request: HttpRequest) -> HttpResponse:
    '''Создаёт новую задачу и привязывает её к текущему юзеру'''
    date_str = request.GET.get('date') or request.POST.get('date')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            if date_str:
                try:
                    task.date = date.fromisoformat(date_str)
                except ValueError:
                    pass
            task.save()
            url = reverse('tasks:task_list')
            if date_str:
                url = f'{url}?date={date_str}'
            return redirect(url)
    else:
        form = TaskForm()

    return render(
        request,
        'tasks/task_form.html',
        {'form': form, 'date_str': date_str}
    )


@require_http_methods(["POST"])
@login_required
def task_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    '''Переключает статус «выполнено» и возвращает обновлённую карточку.'''
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    date_str = request.POST.get('date')
    try:
        selected_date = date.fromisoformat(date_str)
    except (TypeError, ValueError):
        selected_date = timezone.localdate()
    return render(
        request, 
        'tasks/_task_card.html', 
        {'task': task, 'selected_date': selected_date}
    )


@require_http_methods(["POST"])
@login_required
def task_delete(request: HttpRequest, pk: int) -> HttpResponse:
    '''Удаляет задачу текущего юзера и возвращает на список выбранного дня.'''
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    date_str = request.POST.get('date')
    url = reverse('tasks:task_list')
    if date_str:
        url = f'{url}?date={date_str}'
    return redirect(url)


@require_http_methods(["GET", "POST"])
@login_required
def task_edit(request: HttpRequest, pk: int) -> HttpResponse:
    '''Редактирует существующую задачу текущего юзера.'''
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


def register(request: HttpRequest) -> HttpResponse:
    '''Регистрирует нового пользователя и сразу логинит его.'''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks:task_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


