# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class CreateMessagesTest(APITestCase):
    fixtures = ['test_data/users.json', 'test_data/convo_threads.json', 'test_data/convo_messages.json']

    def setUp(self):
        self.client.login(username='john', password='password')

    def test_create_message(self):
        url = '/api/messages/'
        data = {
            "subject": "Nunc feugiat mi a tellus consequat imperdiet.",
            "body": "Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero.",
            "recipient": 2
        }
        expected = {
            "id": 8,
            "subject": "Nunc feugiat mi a tellus consequat imperdiet.",
            "sender": 1,
            "recipient": 2,
            "body": "Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero.",
            "is_read": False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected)

    def test_create_reply_message(self):
        url = '/api/threads/1/messages/'
        data = {
            "body": "Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero.",
        }
        expected = {
            "id": 9,
            "sender": 1,
            "recipient": 2,
            "body": "Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero.",
            "is_read": False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected)

class ReadMessagesTest(APITestCase):
    fixtures = ['test_data/users.json', 'test_data/convo_threads.json', 'test_data/convo_messages.json']

    def setUp(self):
        self.client.login(username='john', password='password')

    def test_view_messages_list_not_allowed(self):
        url = '/api/messages/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_view_message_detail(self):
        url = '/api/messages/1/'
        response = self.client.get(url)
        expected = {
            "id": 1,
            "subject": "Sed cursus ante dapibus diam.",
            "sender": 1,
            "recipient": 2,
            "body": """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris.""",
            "is_read": True
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_view_thread_messages(self):
        url = '/api/threads/1/messages/'
        expected = [
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
            },
            {
                "id": 3,
                "sender": 1,
                "recipient": 2,
                "body_excerpt": "Pellentesque nibh. Aenean quam. In scelerisque se...",
                "is_read": False
            },
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_view_thread_message_detail_not_allowed(self):
        url = '/api/threads/1/messages/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdateMessagesTest(APITestCase):
    fixtures = ['test_data/users.json', 'test_data/convo_threads.json', 'test_data/convo_messages.json']

    def setUp(self):
        self.client.login(username='john', password='password')

    def test_update_message_not_allowed(self):
        url = '/api/messages/1/'
        data = {
            "sender": 1,
            "recipient": 2,
            "subject": "Sed cursus ante dapibus diam.",
            "body": "dummy content"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_thread_message_not_allowed(self):
        url = '/api/threads/1/messages/1/'
        data = {
            "sender": 1,
            "recipient": 2,
            "subject": "Sed cursus ante dapibus diam.",
            "body": "dummy content"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_message(self):
        url = '/api/messages/3/read/'
        expected = {
            "id": 3,
            "subject": "Sed cursus ante dapibus diam.",
            "sender": 1,
            "recipient": 2,
            "body": """Pellentesque nibh. Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor. Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa.""",
            "is_read": True
        }
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_unread_message(self):
        url = '/api/messages/1/unread/'
        expected = {
            "id": 1,
            "subject": "Sed cursus ante dapibus diam.",
            "sender": 1,
            "recipient": 2,
            "body": """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris.""",
            "is_read": False
        }
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)
