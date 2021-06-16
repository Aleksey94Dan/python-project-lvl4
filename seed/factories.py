"""Preparing models for testing."""

from factory import SubFactory, Factory, django
from faker import Factory
import factory
from user.models import CustomUser
from labels.models import Label
from statuses.models import Status
from tasks.models import Task




class UserFactory(django.DjangoModelFactory):

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.Faker('password')

    class Meta:
        model = CustomUser


class StatusFactory(django.DjangoModelFactory):

    name = factory.Faker('name')

    class Meta:
        model = Status


class LabelFactory(django.DjangoModelFactory):

    name = factory.Faker('name')

    class Meta:
        model = Label


class TaskFactory(django.DjangoModelFactory):

    name = factory.Faker('name')
    description = factory.Faker('text', nb_words=200)
    author = SubFactory(UserFactory)
    executor = SubFactory(UserFactory)
    labels = SubFactory(LabelFactory)
    status = SubFactory(StatusFactory)

    class Meta:
        model = Task

