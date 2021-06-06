"""Test filter for task."""


from django.test import TestCase

from labels.models import Label
from statuses.models import Status
from tasks.filter import TaskFilter
from tasks.models import Task
from user.models import CustomUser, User


class FilterTaskTests(TestCase):
    """Test filter."""

    def test_filtering(self):
        s1 = Status.objects.create(name='первый')
        s2 = Status.objects.create(name='второй')
        s3 = Status.objects.create(name='третий')
        l1 = Label.objects.create(name='первая')
        l2 = Label.objects.create(name='вторая')
        l3 = Label.objects.create(name='третья')
        a1 = User.objects.create(
            username='иван',
            first_name='Иван',
            last_name='Иванов',
        )
        a2 = User.objects.create(
            username='петр',
            first_name='Пертр',
            last_name='Петров',
        )
        a3 = User.objects.create(
            username='игорь',
            first_name='Игорь',
            last_name='Петров',
        )
        t1 = Task.objects.create(
            name='первая задача',
            status=s1,
            description='Описание',
            author=CustomUser.objects.get(pk=a1.pk),
            executor=CustomUser.objects.get(pk=a2.pk),
        )
        t1.labels.add(l1.pk)
        t2 = Task.objects.create(
            name='вторая задача',
            status=s2,
            description='Описание',
            author=CustomUser.objects.get(pk=a2.pk),
            executor=CustomUser.objects.get(pk=a1.pk),
        )
        t2.labels.add(l2.pk)
        t3 = Task.objects.create(
            name='третья задача',
            status=s3,
            description='Описание',
            author=CustomUser.objects.get(pk=a3.pk),
            executor=CustomUser.objects.get(pk=a1.pk),
        )
        t3.labels.add(l3.pk)

        qs = Task.objects.all()

        f = TaskFilter(queryset=qs)
        self.assertQuerysetEqual(
            f.qs, [t1.pk, t2.pk, t3.pk], lambda o: o.pk, ordered=False,
        )

        f = TaskFilter({'status': s1.pk}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [t1.pk], lambda o: o.pk)

        f = TaskFilter({'status': s2.pk}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [t2.pk], lambda o: o.pk)

        f = TaskFilter({'executor': a1.pk}, queryset=qs)
        self.assertQuerysetEqual(
            f.qs, [t2.pk, t3.pk], lambda o: o.pk, ordered=False,
        )

        f = TaskFilter({'executor': a2.pk}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [t1.pk], lambda o: o.pk)

        f = TaskFilter({'executor': a3.pk}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [], lambda o: o.pk)

        f = TaskFilter({'label': l1.pk}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [t1.pk], lambda o: o.pk)

        f = TaskFilter({'label': l2.pk}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [t2.pk], lambda o: o.pk)

        f = TaskFilter({'status': s1.pk, 'label': l2.pk}, queryset=qs)
        self.assertQuerysetEqual(f.qs, [], lambda o: o.pk)
