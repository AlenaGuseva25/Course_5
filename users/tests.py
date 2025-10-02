from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from users.models import User
from users.serializers import UserSerializer, TokenSerializer


class UserModelTest(TestCase):
    def test_email_unique(self):
        """Тест уникальности email"""
        User.objects.create(email="unique@example.com", tg_id="11111111")
        with self.assertRaises(Exception):
            User.objects.create(email="unique@example.com", tg_id="22222222")

    def test_tg_id_unique(self):
        """Тест уникальности tg_id"""
        User.objects.create(email="user1@example.com", tg_id="99999999")
        with self.assertRaises(Exception):
            User.objects.create(email="user2@example.com", tg_id="99999999")

    def test_user_creation(self):
        """Тест создания пользователя"""
        user = User.objects.create(
            email="test@example.com",
            tg_id="12345678"
        )
        user.set_password("testpass123")
        user.save()

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.tg_id, "12345678")
        self.assertTrue(user.check_password("testpass123"))

    def test_user_str_method(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create(email="test@example.com")
        self.assertEqual(str(user), "test@example.com")


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_password_write_only(self):
        """Проверка что password write_only"""
        user = User.objects.create(email='existing@example.com')
        user.set_password('testpass')
        user.save()

        serializer = UserSerializer(user)
        self.assertNotIn('password', serializer.data)

    def test_missing_email(self):
        """Проверка ошибки при отсутствии email"""
        invalid_data = {'password': 'testpass123'}
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_missing_password(self):
        """Проверка ошибки при отсутствии password"""
        invalid_data = {'email': 'test@example.com'}
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_valid_serializer_data(self):
        """Тест валидных данных сериализатора"""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())


class TokenSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='tokenuser@example.com')
        self.user.set_password('testpass123')
        self.user.save()

    def test_get_token_contains_email(self):
        """Проверка, что email включен в токен"""
        token = TokenSerializer.get_token(self.user)
        self.assertIn('email', token.payload)
        self.assertEqual(token.payload['email'], 'tokenuser@example.com')

    def test_get_token_contains_tg_id(self):
        """Проверка, что tg_id включен в токен если есть"""

        token = TokenSerializer.get_token(self.user)
        self.assertIn('tg_id', token.payload)

        user_with_tg = User.objects.create(
            email='tguser@example.com',
            tg_id='12345678'
        )
        token_with_tg = TokenSerializer.get_token(user_with_tg)
        self.assertEqual(token_with_tg.payload['tg_id'], '12345678')


class UserAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        url = reverse('users:register')
        response = self.client.post(url, data=self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

        user = User.objects.get(email='test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_login(self):
        """Тест авторизации пользователя"""

        user = User.objects.create(email='test@example.com')
        user.set_password('testpass123')
        user.save()

        url = reverse('users:token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_user_login_invalid_credentials(self):
        """Тест авторизации с неверными данными"""
        url = reverse('users:token_obtain_pair')
        data = {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
