import pytest
from django.contrib.auth.models import User
from tasks.models import Task


@pytest.fixture
def user(db):
    return User.objects.create_user(username='alice', password='pass12345')


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username='bob', password='pass12345')


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client
