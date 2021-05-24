from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user(self):
        """ Test creating a new user with email is successful"""
        email = 'test@gmail.com'
        password = 'pwd'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.role, 1)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_visitor(self):
        """ Test creating a new visitor"""
        email = 'test@gmail.com'
        password = 'pwd'
        visitor = get_user_model().objects.create_visitor(email=email,
                                                          password=password)
        self.assertEqual(visitor.email, email)
        self.assertEqual(visitor.role, 1)
        self.assertTrue(visitor.check_password(password))

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test')

        self.assertEqual(user.role, 5)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_writer(self):
        """Test creating a new writer"""
        user = get_user_model().objects.create_writer(
            'test@gmail.com',
            'test')

        self.assertEqual(user.role, 2)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_moderator(self):
        """Test creating a new moderator"""
        user = get_user_model().objects.create_moderator(
            'test@gmail.com',
            'test')

        self.assertEqual(user.role, 3)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_health_agent(self):
        """Test creating a new health agent"""
        user = get_user_model().objects.create_health_agent(
            'test@gmail.com',
            'test')

        self.assertEqual(user.role, 4)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_staff)
