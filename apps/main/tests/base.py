from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class BaseClassTestCase(TestCase):
    def __init__(self, method_name):
        super().__init__(methodName=method_name)
        self.client = Client()

    @staticmethod
    def reverse(url, *args, **kwargs):
        return reverse(url, *args, **kwargs)
