from urllib import response
from django.test import TestCase
from django.test import Client
import base64
from django.contrib.auth.models import User
from user.models import Task
from django.urls import reverse


class TestGetViews(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create new user
        test_user = User.objects.create_user(
            username="test_user", password="1XISRUkwtuK"
        )
        test_user.save()
        self.task_test = Task.objects.create(user=test_user, task="Testing")
        c = Client()
        c.login(username=test_user.username, password=test_user.password)

    def test_get_task(self):
        login = self.client.login(username="test_user", password="1XISRUkwtuK")
        response = self.client.get("/read")
        self.assertEqual(self.task_test.task, "Testing")
        self.assertEqual(response.status_code, 200)


class TestCreateViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create new user
        test_user = User.objects.create_user(
            username="test_user", password="1XISRUkwtuK"
        )
        test_user.save()
        c = Client()
        c.login(username=test_user.username, password=test_user.password)
        test_task = Task.objects.create(user=test_user, task="Arnissa")
        test_task.save()

    def test_create_task(self):
        login = self.client.login(username="test_user", password="1XISRUkwtuK")
        response = self.client.post("/create")
        self.assertEqual(str(response.context["user"]), "test_user")
        self.assertEqual(response.status_code, 200)


class TestUpdateViews(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create new user
        self.test_user = User.objects.create_user(
            username="test_user", password="1XISRUkwtuK"
        )
        self.test_user.save()
        c = Client()
        c.login(username="test_user", password="1XISRUkwtuK")

    def test_update_task(self):
        login = self.client.login(username="test_user", password="1XISRUkwtuK")
        test_task = Task.objects.create(user=self.test_user, task="testing")
        # Load company options page
        url = reverse("update", args=[test_task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_task.task, "testing")

        url = reverse("update", args=[test_task.id])
        data = {"task": "change"}
        response = self.client.post(url, data)
        test_task.save()
        test_task.refresh_from_db()
        print("REsdsdsdsdsdsdsds      ", response, "task", test_task.task)

        self.assertEqual(response.status_code, 200)


class TestDeleteViews(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create new user
        self.test_user = User.objects.create_user(
            username="test_user", password="1XISRUkwtuK"
        )
        self.test_user.save()
        c = Client()
        c.login(username="test_user", password="1XISRUkwtuK")

    def test_delete_task(self):
        login = self.client.login(username="test_user", password="1XISRUkwtuK")
        test_task = Task.objects.create(user=self.test_user, task="checking")
        test_task.save()
        url = reverse("delete", kwargs={"id": test_task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 302)
