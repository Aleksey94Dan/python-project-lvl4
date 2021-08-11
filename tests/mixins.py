
from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from user.models import User


class TestSetUpMixin:  # noqa: WPS230
    """Basic settings for testing views"""

    fixtures = ['statuses.json', 'users.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.users = User.objects.all()
        self.user = self.users.get(username='123')
        self.client.force_login(self.user)
        self.labels = Label.objects.all()
        self.label = self.labels.first()
        self.statuses = Status.objects.all()
        self.status = self.statuses.first()
        self.tasks = Task.objects.all()
        self.task = self.tasks.filter(author__username='123').first()
        self.task_deletion = self.tasks.filter(author__username='777').first()  # noqa: E501
        self.author = self.user
        self.executor = self.users.first()
