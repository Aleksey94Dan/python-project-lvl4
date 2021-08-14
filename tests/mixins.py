from user.models import User


class AuthMixn:
    """Authorize user."""

    user_name = '123'

    def setUp(self):
        self.users = User.objects.all()
        self.user = self.users.get(username=self.user_name)
        self.client.force_login(self.user)


class FixturesMixin:
    """Test data."""

    fixtures = ['statuses.json', 'users.json', 'labels.json', 'tasks.json']
