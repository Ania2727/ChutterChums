from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from forums.models import Tag, Forum
from users.models import UserProfile


class UserAuthTests(TestCase):
    """These are some simple authentication tests for the user app"""

    def setUp(self):
        self.client = Client()
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        # Create a test tag
        self.tag = Tag.objects.create(name='TestTag')

    def test_signup(self):
        # Count users before signup
        user_count = User.objects.count()

        # Submit signup form
        signup_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.post(reverse('users:signup'), signup_data)

        # Verify redirect to quiz
        self.assertRedirects(response, reverse('users:quiz'))

        # Verify user was created
        self.assertEqual(User.objects.count(), user_count + 1)

        # Verify user is logged in
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_and_profile_access(self):
        """login and accessing the profile page"""
        # Login
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(reverse('users:login'), login_data)

        # Verify redirect to profile
        self.assertRedirects(response, reverse('users:profile'))

        # Verify user is logged in
        self.assertTrue('_auth_user_id' in self.client.session)

        # Access profile page
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_logout(self):
        # Login first
        self.client.login(username='testuser', password='testpassword123')

        # Logout
        response = self.client.get(reverse('users:logout'))

        # Verify redirect to home
        self.assertRedirects(response, reverse('home'))

        # Verify user is logged out
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_auth_persistence_during_quiz(self):
        """authentication persists after the quiz"""
        # Create a new user via signup
        signup_data = {
            'username': 'quizuser',
            'email': 'quiz@example.com',
            'password1': 'quizpassword123',
            'password2': 'quizpassword123',
        }
        self.client.post(reverse('users:signup'), signup_data)

        # Verify user can access quiz
        response = self.client.get(reverse('users:quiz'))
        self.assertEqual(response.status_code, 200)

        # Submit interests
        interests_data = {
            'interests': [str(self.tag.id)]
        }
        response = self.client.post(reverse('users:save_interests'), interests_data)

        # Verify user is still logged in
        self.assertTrue('_auth_user_id' in self.client.session)


class UserProfileTests(TestCase):
    """Tests for user profile functionality"""

    def setUp(self):
        self.client = Client()
        # Create and login a test user
        self.user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='profilepass123'
        )
        self.client.login(username='profileuser', password='profilepass123')

        # Create a forum
        self.forum = Forum.objects.create(
            title='Test Forum',
            description='Test Forum Description',
            creator=self.user
        )

    def test_view_profile(self):
        """Test viewing the user profile"""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, 'profileuser')

    def test_edit_profile(self):
        """Test editing the user profile"""
        # Get the edit profile page
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 200)

        # Submit edit form with bio
        edit_data = {
            'bio': 'This is my test bio',
        }
        response = self.client.post(reverse('users:edit_profile'), edit_data)

        # Verify redirect to profile
        self.assertRedirects(response, reverse('users:profile'))

        # Verify bio was updated
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'This is my test bio')

