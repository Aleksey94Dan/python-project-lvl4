"""Test create tasks."""

from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TestTaskView(TestCase):
    """Test create tasks."""

    def setUp(self):
        """Preparate data."""
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.status = Status.objects.create(name='Первый статус')
        self.status.save()
        self.labels = Label.objects.create(name='Первая метка')
        self.labels.save()
        self.task = Task.objects.create(
            name='Тест',
            author=User.objects.get(pk=self.user.pk),
        )
        self.task.save()
        self.url_delete = reverse_lazy(
            'tasks-delete',
            kwargs={'pk': self.task.pk},
        )
        self.url_update = reverse_lazy(
            'tasks-update',
            kwargs={'pk': self.task.pk},
        )
        self.client = Client()

    def test_create(self):
        """Test create tasks."""
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.get(reverse_lazy('tasks-create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        task = {
            'name': 'Тестовая задача',
            'status': self.status.pk,
            'labels': self.labels.pk,
            'description': 'Описание',
            'author': self.user.pk,
            'executor': self.user.pk,
        }
        response = self.client.post(
            reverse_lazy('tasks-create'),
            data=task,
        )
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertTrue(Task.objects.filter(name=task['name']))

        response = self.client.post(
            reverse_lazy('tasks-create'),
            data=task,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete(self):
        """Test delete tasks."""
        self.assertTrue(Task.objects.filter(name='Тест'))
        response = self.client.get(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(self.url_delete)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertFalse(Task.objects.filter(name='Тест'))

    def test_update(self):
        """Test update tasks."""
        self.assertTrue(Task.objects.filter(name='Тест'))
        response = self.client.get(self.url_update)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        task = {
            'name': 'Тсет',
            'status': self.status.pk,
            'labels': self.labels.pk,
            'description': 'Описание',
            'author': self.user.pk,
            'executor': self.user.pk,
        }
        response = self.client.post(
            self.url_update,
            data=task,
        )
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertTrue(Task.objects.filter(name='Тсет'))
