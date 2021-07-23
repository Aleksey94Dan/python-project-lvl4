"""Test tasks of views"""

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from labels.models import Label
from statuses.models import Status
from tasks.filter import TaskFilter
from tasks.models import Task
from user.models import User


class TestTasksView(TestCase):
    """CRUD tests"""

    fixtures = ['statuses.json', 'users.json', 'labels.json', 'tasks.json']

    def assert_tasks_in_html(self, tasks, html):
        for task in tasks:
            self.assertInHTML(str(task.id), html)
            self.assertInHTML(task.name, html)
            self.assertInHTML(task.status.name, html)
            self.assertInHTML(task.author.get_full_name(), html)
            self.assertInHTML(task.executor.get_full_name(), html)

    def test_tasks_list(self):
        self.client.login(username='123', password='123')
        tasks = Task.objects.all()
        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assert_tasks_in_html(tasks, response.content.decode())

    def test_create_task(self):
        self.client.login(username='123', password='123')
        status = Status.objects.all()[:1][0]
        label = Label.objects.all()[:1][0]
        executor = User.objects.get(pk=18)
        response = self.client.post(
            reverse_lazy('tasks-create'),
            follow=True,
            data={
                'name': 'demo',
                'description': 'demo',
                'status': status.pk,
                'labels': label.pk,
                'executor': executor.pk,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Task successfully created',
            response.content.decode(),
        )
        self.assertTrue(Task.objects.filter(name='demo'))

    def test_create_same_task(self):
        self.client.login(username='123', password='123')
        status = Status.objects.all()[:1][0]
        label = Label.objects.all()[:1][0]
        executor = User.objects.get(pk=18)
        response = self.client.post(
            reverse_lazy('tasks-create'),
            follow=True,
            data={
                'name': 'First task',
                'description': 'demo',
                'status': status.pk,
                'labels': label.pk,
                'executor': executor.pk,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Task with this Name already exists.',
            response.content.decode(),
        )

    def test_update_same_task(self):
        self.client.login(username='123', password='123')
        status = Status.objects.all()[:1][0]
        label = Label.objects.all()[:1][0]
        executor = User.objects.get(pk=18)
        response = self.client.post(
            reverse_lazy('tasks-update', kwargs={'pk': 27}),
            follow=True,
            data={
                'name': 'Third task',
                'description': 'demo',
                'status': status.pk,
                'labels': label.pk,
                'executor': executor.pk,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Task successfully changed',
            response.content.decode(),
        )
        self.assertTrue(Task.objects.filter(name='Third task'))

    def test_delete_task(self):
        self.client.login(username='123', password='123')
        response = self.client.post(
            reverse_lazy('tasks-delete', kwargs={'pk': 27}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Task successfully deleted',
            response.content.decode(),
        )
        self.assertFalse(Task.objects.filter(pk=27))

    def test_task_error404(self):
        self.client.login(username='123', password='123')

        for url in ['tasks-delete', 'tasks-update']:
            response = self.client.post(
                reverse_lazy(url, kwargs={'pk': 999}),
                follow=True,
            )
            self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_only_author(self):
        self.client.login(username='456', password='456')
        response = self.client.post(
            reverse_lazy('tasks-delete', kwargs={'pk': 27}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'A task can only be deleted by its author',
            response.content.decode(),
        )
        self.assertTrue(Task.objects.filter(pk=27))

    def test_filter(self):
        self.client.login(username='123', password='123')

        qs = Task.objects.all()

        f = TaskFilter(queryset=qs)
        self.assertQuerysetEqual(
            f.qs, [27, 28, 29, 30], lambda o: o.pk, ordered=False,
        )

        f = TaskFilter({'status': 6}, queryset=qs)
        self.assertQuerysetEqual(
            f.qs, [27, 28], lambda o: o.pk, ordered=False,
        )

        f = TaskFilter({'status': 13}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [], lambda o: o.pk)

        f = TaskFilter({'executor': 11}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [30], lambda o: o.pk)

        f = TaskFilter({'executor': 20}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [], lambda o: o.pk)

        f = TaskFilter({'label': 25}, queryset=qs)
        self.assertQuerysetEqual(
            f.qs, [27, 28, 29], lambda o: o.pk, ordered=False,
        )

        f = TaskFilter({'label': 29}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [], lambda o: o.pk)
