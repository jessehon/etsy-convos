# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class CreateThreadsTest(APITestCase):
    fixtures = ['test_data/users.json', 'test_data/convo_threads.json', 'test_data/convo_messages.json']

    def setUp(self):
        self.client.login(username='john', password='password')

    def test_create_thread_not_allowed(self):
        url = '/api/threads/'
        data = {
            "subject": "dummy data"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class ReadThreadsTest(APITestCase):
    fixtures = ['test_data/users.json', 'test_data/convo_threads.json', 'test_data/convo_messages.json']

    def setUp(self):
        self.client.login(username='john', password='password')

    def test_view_thread_list(self):
        url = '/api/threads/'
        expected = [
            {
                "id": 1,
                "subject": "Sed cursus ante dapibus diam.",
                "last_message": {
                    "id": 2,
                    "sender": 2,
                    "recipient": 1,
                    "body_excerpt": "Fusce nec tellus sed augue semper porta. Mauris m...",
                    "is_read": False
                }
            },
            {
                "id": 2,
                "subject": "Class aptent taciti sociosqu ad litora torquent per conubia nostra",
                "last_message": {
                    "id": 5,
                    "sender": 1,
                    "recipient": 3,
                    "body_excerpt": "Aenean quam. In scelerisque sem at dolor. Maecena...",
                    "is_read": False
                }
            }
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_view_thread_detail(self):
        url = '/api/threads/1/'
        expected = {
            "id": 1,
            "subject": "Sed cursus ante dapibus diam.",
            "messages": [
                {
                    "id": 1,
                    "sender": 1,
                    "recipient": 2,
                    "body_excerpt": "Lorem ipsum dolor sit amet, consectetur adipiscin...",
                    "is_read": True
                },
                {
                    "id": 2,
                    "sender": 2,
                    "recipient": 1,
                    "body_excerpt": "Fusce nec tellus sed augue semper porta. Mauris m...",
                    "is_read": False
                }
            ]
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)
