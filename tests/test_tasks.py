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

    def test_tasks_ticket(self):
        self.client.login(username='123', password='123')
        task = Task.objects.all()[0]
        response = self.client.get(
            reverse_lazy('task-ticket', kwargs={'pk': task.id}),
        )
        html = response.content.decode()

        self.assertInHTML(task.name, html)
        self.assertInHTML(task.author.get_full_name(), html)
        self.assertInHTML(task.status.name, html)
        for t in task.labels.all():
            self.assertInHTML(t.name, html)

    def test_create_task(self):
        self.client.login(username='123', password='123')
        status = Status.objects.all()[:1][0]
        label = Label.objects.all()[:1][0]
        executor = User.objects.all()[:1][0]
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
        self.assertTrue(Task.objects.filter(
            name='demo',
            description='demo',
            status=status.pk,
            labels=label.pk,
            executor=executor.pk,
        ),
        )

    def test_create_same_task(self):
        self.client.login(username='123', password='123')
        status = Status.objects.all()[:1][0]
        label = Label.objects.all()[:1][0]
        executor = User.objects.all()[:1][0]
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
        self.assertFalse(Task.objects.filter(
            name='First task',
            description='demo',
            status=status.pk,
            labels=label.pk,
            executor=executor.pk,
        ),
        )

    def test_update_same_task(self):
        self.client.login(username='123', password='123')
        status = Status.objects.all()[:1][0]
        label = Label.objects.all()[:1][0]
        executor = User.objects.all()[:1][0]
        task = Task.objects.filter(author__username='123')[0]
        response = self.client.post(
            reverse_lazy('tasks-update', kwargs={'pk': task.pk}),
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
        self.assertTrue(Task.objects.filter(
            name='Third task',
            description='demo',
            status=status.pk,
            labels=label.pk,
            executor=executor.pk,
        ),
        )

    def test_delete_task(self):
        self.client.login(username='123', password='123')
        task = Task.objects.filter(author__username='123')[0]
        response = self.client.post(
            reverse_lazy('tasks-delete', kwargs={'pk': task.pk}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Task successfully deleted',
            response.content.decode(),
        )
        self.assertFalse(Task.objects.filter(pk=task.pk))

    def test_task_error404(self):
        self.client.login(username='123', password='123')
        last_task = Task.objects.all().order_by('-pk')[0]

        for url in ['tasks-delete', 'tasks-update']:
            response = self.client.post(
                reverse_lazy(url, kwargs={'pk': last_task.id + 1}),
                follow=True,
            )
            self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_only_author(self):
        self.client.login(username='456', password='456')
        task = Task.objects.exclude(author__username='456')[0]
        response = self.client.post(
            reverse_lazy('tasks-delete', kwargs={'pk': task.id}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'A task can only be deleted by its author',
            response.content.decode(),
        )
        self.assertTrue(Task.objects.filter(pk=task.id))

    def test_filter(self):
        self.client.login(username='123', password='123')

        qs = Task.objects.all()
        ids = list(map(lambda x: x.id, qs))

        f = TaskFilter(queryset=qs)
        self.assertQuerysetEqual(f.qs, ids, lambda o: o.pk, ordered=False)

        status = Status.objects.all()[0]
        ids = list(map(lambda x: x.id, qs.filter(status=status)))
        f = TaskFilter({'status': status.pk}, queryset=qs)
        self.assertQuerysetEqual(f.qs, ids, lambda o: o.pk, ordered=False)

        executor = User.objects.get(username='123')
        ids = list(map(lambda x: x.id, qs.filter(executor=executor)))
        f = TaskFilter({'executor': executor.pk}, queryset=qs)
        self.assertQuerysetEqual(f.qs, ids, lambda o: o.pk)

        label = Label.objects.all()[0]
        ids = list(map(lambda x: x.id, qs.filter(labels=label)))
        f = TaskFilter({'label': label.id}, queryset=qs)
        self.assertQuerysetEqual(f.qs, ids, lambda o: o.pk, ordered=False)
