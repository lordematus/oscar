from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from messaging.models import Message


class UserViewSetTest(APITestCase):
    pass


class MessageViewSetTest(APITestCase):
    def setUp(self):
        self.url = reverse('message-list')
        self.user1 = User.objects.create(
            username="ana",
            email="ana@email.com",
            password="ana123",
        )
        self.user2 = User.objects.create(
            username="bob",
            email="bob@email.com",
            password="bob123"
        )

    def test_list_messages_with_unauthenticated_user(self):
        response = self.client.get(path=self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('Authentication credentials were not provided.', response.data['detail'])

    def test_list_message_successfully(self):
        m1 = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Hi'
        )
        m2 = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Hello'
        )

        self.client.force_authenticate(self.user1)
        response = self.client.get(path=self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(m2.recipient.pk, response.data[0]['recipient'])
        self.assertEqual(m2.content, response.data[0]['content'])
        self.assertEqual(m1.recipient.pk, response.data[1]['recipient'])
        self.assertEqual(m1.content, response.data[1]['content'])

    def test_create_message_with_unauthenticated_user(self):
        response = self.client.post(path=self.url, format='json', data={
            'recipient': self.user2.pk,
            'content': 'Hello',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Authentication credentials were not provided.', response.data['detail'])
        self.assertEqual(Message.objects.count(), 0)

    def test_create_message_sucessfully(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(path=self.url, format='json', data={
            'recipient': self.user2.pk,
            'content': 'Hello',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['recipient'], self.user2.pk)
        self.assertEqual(response.data['content'], 'Hello')

        message = Message.objects.get()
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.recipient, self.user2)
        self.assertEqual(message.content, 'Hello')

    def test_create_message_user_not_existent(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(path=self.url, format='json', data={
            'recipient': 0,
            'content': 'Hello'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid pk "0" - object does not exist.', response.data['recipient'])
        self.assertEqual(Message.objects.count(), 0)

    def test_cannot_create_message_with_user_sender_and_recipient(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(path=self.url, format='json', data={
            'recipient': self.user1.pk,
            'content': 'Hello'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cannot send message to yourself', response.data['recipient'])
        self.assertEqual(Message.objects.count(), 0)
