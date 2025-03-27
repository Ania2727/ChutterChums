from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import UserProfile


class UserAccountTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('users:signup')
        self.login_url = reverse('users:login')
        self.profile_url = reverse('users:profile')
        self.quiz_url = reverse('users:quiz')

        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }

    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect to quiz/profile
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='testuser').exists())

    def test_user_login(self):
        User.objects.create_user(username='testlogin', email='login@test.com', password='pass1234')
        response = self.client.post(self.login_url, {'username': 'testlogin', 'password': 'pass1234'})
        self.assertEqual(response.status_code, 302)  # Redirect to profile
        self.assertRedirects(response, self.profile_url)

    def test_quiz_access_requires_login(self):
        # Should redirect to login if not logged in
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('users:login')))

        # Login and try again
        self.client.post(self.signup_url, self.user_data)
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz.html')

    def test_profile_auto_created(self):
        user = User.objects.create_user(username='autouser', email='auto@test.com', password='pass1234')
        self.assertTrue(hasattr(user, 'userprofile'))
