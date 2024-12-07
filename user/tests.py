from django.test import TestCase, Client
from django.urls import reverse
from .factories import CustomUserFactory
from .models import CustomUser
from .forms import RegistrationForm, LoginForm
from datetime import date

class UserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()

    def test_user_data(self):
        self.assertTrue(self.user.username)
        self.assertTrue(self.user.email)
        self.assertTrue(self.user.birth_date)


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUserFactory()

    def test_profile_detail_view(self):
        response = self.client.get(reverse('profile', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')
        self.assertEqual(response.context['object'], self.user)

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_view_post_valid_form(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'test@example.com',
            'birth_date': '1990-01-01',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.birth_date, date(1990, 1, 1))

    def test_register_view_post_invalid_form(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
            'email': 'test@example.com',
            'birth_date': '1990-01-01',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
        self.assertEqual(CustomUser.objects.count(), 0)

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = CustomUserFactory(username='testuser', password='testpassword123')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_view_post_valid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')
        self.user = CustomUserFactory(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')

    def test_logout_view(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(response.wsgi_request.user.is_authenticated)