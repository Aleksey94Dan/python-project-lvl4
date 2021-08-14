"""Test tasks of views"""

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from labels.models import Label
from statuses.models import Status
from tasks.filter import TaskFilter
from tasks.models import Task
from tests.mixins import AuthMixn, FixturesMixin


class TestTasksView(FixturesMixin, AuthMixn, TestCase):
    """CRUD tests"""

    other_user_name = '777'

    def setUp(self):
        super().setUp()
        self.statuses = Status.objects.all()
        self.status = self.statuses.first()
        self.labels = Label.objects.all()
        self.label = self.labels.first()
        self.tasks = Task.objects.all()
        self.task = self.tasks.filter(
            author__username=self.user_name,
        ).first()
        self.task_deletion = self.tasks.filter(
            author__username=self.other_user_name,
        ).first()  # noqa: E501
        self.author = self.user
        self.executor = self.users.first()

    def assert_tasks_in_html(self, tasks, html):
        for task in tasks:
            self.assertInHTML(str(task.id), html)
            self.assertInHTML(task.name, html)
            self.assertInHTML(task.status.name, html)
            self.assertInHTML(task.author.get_full_name(), html)
            self.assertInHTML(task.executor.get_full_name(), html)

    def test_tasks_list(self):
        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assert_tasks_in_html(self.tasks, response.content.decode())

    def test_tasks_ticket(self):
        response = self.client.get(
            reverse_lazy('task-ticket', kwargs={'pk': self.task.id}),
        )
        html = response.content.decode()

        self.assertInHTML(self.task.name, html)
        self.assertInHTML(self.task.author.get_full_name(), html)
        self.assertInHTML(self.task.status.name, html)
        for t in self.task.labels.all():
            self.assertInHTML(t.name, html)

    def test_create_task(self):
        response = self.client.post(
            reverse_lazy('tasks-create'),
            follow=True,
            data={
                'name': 'demo',
                'description': 'demo',
                'status': self.status.pk,
                'labels': self.label.pk,
                'executor': self.executor.pk,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Task successfully created',
            response.content.decode(),
        )
        self.assertTrue(self.tasks.filter(
            name='demo',
            description='demo',
            status=self.status.pk,
            labels=self.label.pk,
            executor=self.executor.pk,
        ).exists(),
        )

    def test_create_same_task(self):
        response = self.client.post(
            reverse_lazy('tasks-create'),
            follow=True,
            data={
                'name': 'First task',
                'description': 'demo',
                'status': self.status.pk,
                'labels': self.label.pk,
                'executor': self.executor.pk,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Task with this Name already exists.',
            response.content.decode(),
        )
        self.assertFalse(self.tasks.filter(
            name='First task',
            description='demo',
            status=self.status.pk,
            labels=self.label.pk,
            executor=self.executor.pk,
        ),
        )

    def test_update_same_task(self):
        response = self.client.post(
            reverse_lazy('tasks-update', kwargs={'pk': self.task.pk}),
            follow=True,
            data={
                'name': 'Third task',
                'description': 'demo',
                'status': self.status.pk,
                'labels': self.label.pk,
                'executor': self.executor.pk,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Task successfully changed',
            response.content.decode(),
        )
        self.assertTrue(self.tasks.filter(
            name='Third task',
            description='demo',
            status=self.status.pk,
            labels=self.label.pk,
            executor=self.executor.pk,
        ),
        )

    def test_delete_task(self):
        response = self.client.post(
            reverse_lazy('tasks-delete', kwargs={'pk': self.task.pk}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Task successfully deleted',
            response.content.decode(),
        )
        self.assertFalse(self.tasks.filter(pk=self.task.pk).exists())

    def test_task_error404(self):
        fake_id = 9999
        for url in ['tasks-delete', 'tasks-update']:
            response = self.client.post(
                reverse_lazy(url, kwargs={'pk': fake_id}),
                follow=True,
            )
            self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_only_author(self):
        task = self.task_deletion
        response = self.client.post(
            reverse_lazy('tasks-delete', kwargs={'pk': task.id}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'A task can only be deleted by its author',
            response.content.decode(),
        )
        self.assertTrue(self.tasks.filter(pk=task.id).exists())

    def test_filter(self):
        qs = self.tasks
        status = self.status
        executor = self.executor
        label = self.label

        task_ids = list(map(lambda x: x.id, qs))
        status_ids = list(map(lambda x: x.id, qs.filter(status=status)))
        executor_ids = list(map(lambda x: x.id, qs.filter(executor=executor)))
        label_ids = list(map(lambda x: x.id, qs.filter(labels=label)))

        f_all = TaskFilter(queryset=qs)
        f_statuses = TaskFilter({'status': status.pk}, queryset=qs)
        f_executors = TaskFilter({'executor': executor.pk}, queryset=qs)
        f_labels = TaskFilter({'label': label.id}, queryset=qs)

        self.assertQuerysetEqual(
            f_all.qs, task_ids, lambda o: o.pk, ordered=False,
        )
        self.assertQuerysetEqual(
            f_statuses.qs, status_ids, lambda o: o.pk, ordered=False,
        )
        self.assertQuerysetEqual(f_executors.qs, executor_ids, lambda o: o.pk)
        self.assertQuerysetEqual(
            f_labels.qs, label_ids, lambda o: o.pk, ordered=False,
        )
