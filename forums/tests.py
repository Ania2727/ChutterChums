from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from forums.models import Forum, Topic, Comment, Tag
from forums.forms import CreateInForum, TopicForm, CommentForm


class ModelTests(TestCase):
    """Some tests of relatively basic forum functionality"""

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create a forum
        self.forum = Forum.objects.create(
            creator=self.user,
            title='Test Forum',
            description='A description'
        )

        # Add the creator as a member
        self.forum.members.add(self.user)

        # Create a tag
        self.tag = Tag.objects.create(name='Technology')

        # Add tag to forum
        self.forum.tags.add(self.tag)

        # Create a topic
        self.topic = Topic.objects.create(
            forum=self.forum,
            author=self.user,
            title='Test Topic',
            content='A topic'
        )

        # Create a comment
        self.comment = Comment.objects.create(
            topic=self.topic,
            author=self.user,
            content='A comment'
        )

    def test_forum_creation(self):
        self.assertEqual(self.forum.title, 'Test Forum')
        self.assertEqual(self.forum.description, 'A description')
        self.assertEqual(self.forum.creator, self.user)
        self.assertEqual(self.forum.tags.count(), 1)
        self.assertEqual(self.forum.members.count(), 1)

    def test_topic_creation(self):
        self.assertEqual(self.topic.title, 'Test Topic')
        self.assertEqual(self.topic.content, 'A topic')
        self.assertEqual(self.topic.author, self.user)
        self.assertEqual(self.topic.forum, self.forum)
        self.assertEqual(self.topic.views, 0)

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'A comment')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.topic, self.topic)

    def test_string_representations(self):
        self.assertEqual(str(self.forum), 'Test Forum')
        self.assertEqual(str(self.topic), 'Test Topic')
        self.assertEqual(str(self.tag), 'Technology')
        expected_comment_str = f'Comment by {self.user.username} on {self.topic.title}'
        self.assertEqual(str(self.comment), expected_comment_str)


class ViewTests(TestCase):
    """This tests some simple cases for views"""

    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create another user for permission tests
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )

        # Create a forum
        self.forum = Forum.objects.create(
            creator=self.user,
            title='Test Forum',
            description='This is a test forum description'
        )

        # Add user as member
        self.forum.members.add(self.user)

        # Create a topic
        self.topic = Topic.objects.create(
            forum=self.forum,
            author=self.user,
            title='Test Topic',
            content='This is test content for the topic'
        )

        # URLs
        self.forum_list_url = reverse('forums:forum_list')
        self.forum_detail_url = reverse('forums:forum_detail', args=[self.forum.id])
        self.topic_detail_url = reverse('forums:topic_detail', args=[self.forum.id, self.topic.id])
        self.create_topic_url = reverse('forums:create_topic', args=[self.forum.id])
        self.edit_topic_url = reverse('forums:edit_topic', args=[self.forum.id, self.topic.id])

    def test_protected_views_require_login(self):
        # Create topic (should redirect or return 302/403)
        response = self.client.get(self.create_topic_url)
        self.assertNotEqual(response.status_code, 200)

        # Edit topic (should redirect or return 302/403)
        response = self.client.get(self.edit_topic_url)
        self.assertNotEqual(response.status_code, 200)


class FormTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create a forum
        self.forum = Forum.objects.create(
            creator=self.user,
            title='Test Forum',
            description='This is a test forum description'
        )

        # Create a topic
        self.topic = Topic.objects.create(
            forum=self.forum,
            author=self.user,
            title='Test Topic',
            content='This is test content for the topic'
        )

    def test_form_validation(self):
        """Some form validation for user inputs"""
        # Forum Creation Form
        valid_forum_data = {
            'title': 'New Forum',
            'description': 'This is a new forum',
        }
        invalid_forum_data = {
            'description': 'Missing title',
        }

        valid_forum_form = CreateInForum(data=valid_forum_data, user=self.user)
        invalid_forum_form = CreateInForum(data=invalid_forum_data, user=self.user)

        self.assertTrue(valid_forum_form.is_valid())
        self.assertFalse(invalid_forum_form.is_valid())

        # Topic Form
        valid_topic_data = {
            'title': 'New Topic',
            'content': 'This is content for the new topic',
        }
        invalid_topic_data = {
            'title': 'Missing content',
        }

        valid_topic_form = TopicForm(data=valid_topic_data, user=self.user, forum=self.forum)
        invalid_topic_form = TopicForm(data=invalid_topic_data, user=self.user, forum=self.forum)

        self.assertTrue(valid_topic_form.is_valid())
        self.assertFalse(invalid_topic_form.is_valid())

        # Comment Form
        valid_comment_data = {
            'content': 'This is a new comment',
        }
        invalid_comment_data = {}

        valid_comment_form = CommentForm(data=valid_comment_data, user=self.user, topic=self.topic)
        invalid_comment_form = CommentForm(data=invalid_comment_data, user=self.user, topic=self.topic)

        self.assertTrue(valid_comment_form.is_valid())
        self.assertFalse(invalid_comment_form.is_valid())
