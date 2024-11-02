from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, StudentLoginForm

class UserRegistrationFormTest(TestCase):
    def test_password_mismatch(self):
        form_data = {
            'username': 'student',
            'password': 'password123',
            'password2': 'differentpassword'
        }
        form = UserRegistrationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["Passwords don't match."])