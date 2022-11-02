from django.test import TestCase
from user.models import Task
from django.contrib.auth.models import User


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="Hannan", password="54321")
        Task.objects.create(user=user, task="Testing app")

    def test_obj_name(self):
        task_obj = Task.objects.get(task="Testing app")
        test_var = task_obj.task
        self.assertEqual(str(task_obj), test_var)
