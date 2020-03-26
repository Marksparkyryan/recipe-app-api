from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test2@email.com', password='testpass2'):
    """Create sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a new user with an email is usccessful"""
        email = 'sparky@email.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test for new user's email normalized"""
        email = 'sparky@EMaiL.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='password123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_onvalid_email(self):
        """test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string representation"""
        tag = models.Tag.objects.create(
            name='Vegan',
            user=sample_user(),
        )
        
        self.assertEqual(str(tag), tag.name)
    
    