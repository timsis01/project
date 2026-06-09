import pytest
from django.urls import reverse
from tasks.models import Task


def test_task_list_requires_login(client):
    '''Незалогиненного редиректит на страницу логина'''
    response = client.get(reverse('tasks:task_list'))
    assert response.status_code == 302
    assert '/login' in response.url


def test_user_sees_only_own_tasks(auth_client, user, other_user):
    '''Юзер не видит чужие задачи'''
    my_task = Task.objects.create(title='Моя задача', user=user)
    Task.objects.create(title='Чужая задача', user=other_user)

    response = auth_client.get(reverse('tasks:task_list'))

    assert response.status_code == 200
    tasks = list(response.context['tasks'])
    assert tasks == [my_task]


def test_cannot_toggle_other_users_task(auth_client, other_user):
    '''Юзер не меняет чужие задачи'''
    other_task = Task.objects.create(title='Чужая', user=other_user)

    url = reverse('tasks:task_toggle', args=[other_task.pk])
    response = auth_client.post(url)

    assert response.status_code == 404
    other_task.refresh_from_db()
    assert other_task.is_done is False  # статус не изменился


def test_toggle_marks_task_done(auth_client, user):
    '''POST на task_toggle переключает is_done в таске юзера.'''
    task = Task.objects.create(title='Сделать', user=user, is_done=False)

    url = reverse('tasks:task_toggle', args=[task.pk])
    response = auth_client.post(url)

    assert response.status_code == 200
    task.refresh_from_db()
    assert task.is_done is True


def test_create_task_assigns_current_user(auth_client, user):
    '''Созданная задача принадлежит залогиненному юзеру'''
    url = reverse('tasks:task_create')
    response = auth_client.post(
        url, 
        {'title': 'Новая задача', 'description': ''}
    )

    assert response.status_code == 302  # успех → редирект на список
    task = Task.objects.get(title='Новая задача')
    assert task.user == user


