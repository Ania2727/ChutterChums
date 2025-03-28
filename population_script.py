import os
import sys
import random
import django
from django.db import IntegrityError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatterchums.settings')
django.setup()

# Import Django models (must be after django.setup())
from django.utils import timezone
from django.contrib.auth.models import User

from forums.models import Tag, Forum, Topic, Comment


def populate_tags():
    tags = [
        'Technology', 'Gaming', 'Entertainment', 'Sports', 'Science',
        'Art', 'Music', 'Movies', 'Books', 'Food', 'Travel', 'Fashion',
        'Health', 'Fitness', 'Politics', 'Business', 'Finance', 'Education',
        'TV Shows', 'Anime', 'Comics', 'Podcasts', 'Celebrities',
        'Rock', 'Pop', 'Hip-Hop', 'Jazz', 'Classical', 'Electronic',
        'Humor', 'News', 'History', 'Philosophy', 'Psychology'
    ]

    created_count = 0
    existing_count = 0

    for tag_name in tags:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            created_count += 1
            print(f"Created tag: {tag_name}")
        else:
            existing_count += 1

    print(f"\nTag population summary:")
    print(f"Created: {created_count}")
    print(f"Already existed: {existing_count}")
    print(f"Total tags: {len(tags)}")

    return Tag.objects.all()


def create_users():
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'password': '!securepassword1'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'password': '£securepassword2'},
        {'username': 'alex_tech', 'email': 'alex@example.com', 'password': '$securepassword3'},
        {'username': 'sam_gamer', 'email': 'sam@example.com', 'password': '!securepassword4'},
        {'username': 'taylor_music', 'email': 'taylor@example.com', 'password': '£securepassword5'},
        {'username': 'jordan_sports', 'email': 'jordan@example.com', 'password': '$securepassword6'},
        {'username': 'robin_books', 'email': 'robin@example.com', 'password': '!securepassword7'},
        {'username': 'casey_travel', 'email': 'casey@example.com', 'password': '$securepassword8'},
    ]

    created_users = []
    created_count = 0
    existing_count = 0

    for user_data in users_data:
        try:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                email=user_data['email'],
                defaults={'is_active': True}
            )

            if created:
                user.set_password(user_data['password'])
                user.save()
                created_count += 1
                print(f"Created user: {user.username}")
            else:
                existing_count += 1

            created_users.append(user)

        except IntegrityError:
            print(f"Error creating user {user_data['username']}, skipping...")

    print(f"\nUser creation summary:")
    print(f"Created: {created_count}")
    print(f"Already existed: {existing_count}")
    print(f"Total users: {len(created_users)}")

    return created_users


def create_forums(users, tags):
    forums_data = [
        {
            'title': 'Tech Enthusiasts',
            'description': 'A place to discuss the latest technology trends and innovations.',
            'tag_names': ['Technology', 'Science', 'Education'],
        },
        {
            'title': 'Gaming Hub',
            'description': 'Share your gaming experiences, tips, and discover new games.',
            'tag_names': ['Gaming', 'Entertainment', 'Technology'],
        },
        {
            'title': 'Music Lovers',
            'description': 'For those who appreciate all genres of music.',
            'tag_names': ['Music', 'Rock', 'Pop', 'Jazz', 'Classical', 'Hip-Hop'],
        },
        {
            'title': 'Book Club',
            'description': 'Discuss your favorite books and discover new reads.',
            'tag_names': ['Books', 'Education', 'Entertainment'],
        },
        {
            'title': 'Travel Adventures',
            'description': 'Share your travel stories and get inspiration for your next trip.',
            'tag_names': ['Travel', 'Food', 'Photography'],
        },
        {
            'title': 'Fitness Journey',
            'description': 'Support and motivation for your fitness goals.',
            'tag_names': ['Fitness', 'Health', 'Sports'],
        },
        {
            'title': 'Movie Buffs',
            'description': 'Discussions about movies, directors, and actors.',
            'tag_names': ['Movies', 'Entertainment', 'Celebrities'],
        },
    ]

    created_forums = []
    created_count = 0
    existing_count = 0

    # Get tag objects by name
    tag_dict = {tag.name: tag for tag in tags}

    for forum_data in forums_data:
        creator = random.choice(users)

        # Check if forum already exists
        existing_forum = Forum.objects.filter(title=forum_data['title']).first()

        if existing_forum:
            existing_count += 1
            created_forums.append(existing_forum)
            continue

        # Create new forum
        new_forum = Forum.objects.create(
            creator=creator,
            name=creator.username,
            title=forum_data['title'],
            description=forum_data['description'],
            date_posted=timezone.now()
        )

        # Save forum first before adding many-to-many relationships
        new_forum.save()

        # Add tags
        for tag_name in forum_data['tag_names']:
            if tag_name in tag_dict:
                new_forum.tags.add(tag_dict[tag_name])

        # Add creator as member
        new_forum.members.add(creator)

        # Add random members (between 2 and 6 additional members)
        potential_members = [u for u in users if u != creator]
        member_count = min(len(potential_members), random.randint(2, 6))
        random_members = random.sample(potential_members, member_count)

        for member in random_members:
            new_forum.members.add(member)

        created_count += 1
        created_forums.append(new_forum)
        print(f"Created forum: {new_forum.title}")

    print(f"\nForum creation summary:")
    print(f"Created: {created_count}")
    print(f"Already existed: {existing_count}")
    print(f"Total forums: {len(created_forums)}")

    return created_forums


def create_topics_and_comments(forums):
    sample_topics = [
        {
            'title': 'Welcome to our community!',
            'content': 'Hello everyone! Welcome to our forum. Feel free to introduce yourself and share your interests.',
        },
        {
            'title': 'Forum Rules',
            'content': 'Please review our community guidelines: Be respectful, no spam, and have fun!',
        },
        {
            'title': 'What brought you here?',
            'content': "I'm curious to know what brought everyone to this community. Share your story!",
        },
        {
            'title': 'Monthly Discussion Thread',
            'content': "This month's topic is all about your favorite experiences. Let's share and discuss!",
        },
        {
            'title': 'Looking for recommendations',
            'content': "I'm new to this area and looking for recommendations. What are your favorites?",
        },
        {
            'title': 'Upcoming Events',
            'content': "Let's compile a list of upcoming events related to our interests. Share anything you know about!",
        },
    ]

    sample_comments = [
        "Great post! I completely agree with your points.",
        "Thanks for sharing this information. It was very helpful.",
        "I had a similar experience and can relate to this.",
        "Interesting perspective. I hadn't thought about it that way.",
        "I have a question about your post. Can you clarify?",
        "This is exactly what I needed to know!",
        "I disagree with some points, but appreciate the discussion.",
        "Has anyone else experienced this issue?",
        "I'm new here, but this seems like a great community.",
        "Looking forward to more posts like this one!",
    ]

    topics_created = 0
    comments_created = 0

    for forum in forums:
        # Create 2-4 topics per forum
        topic_count = random.randint(2, 4)
        forum_topics = random.sample(sample_topics, min(topic_count, len(sample_topics)))

        for topic_data in forum_topics:
            # Get members of the forum
            members = forum.members.all()
            if not members:
                author = forum.creator
            else:
                author = random.choice(list(members))

            # Create topic
            topic = Topic.objects.create(
                forum=forum,
                author=author,
                title=topic_data['title'],
                content=topic_data['content'],
                views=random.randint(5, 50)
            )
            topics_created += 1

            # Create 2-6 comments per topic
            comment_count = random.randint(2, 6)

            for _ in range(comment_count):
                members = forum.members.all()
                if not members:
                    comment_author = forum.creator
                else:
                    comment_author = random.choice(list(members))
                comment_text = random.choice(sample_comments)

                Comment.objects.create(
                    topic=topic,
                    author=comment_author,
                    content=comment_text
                )
                comments_created += 1

    print(f"\nContent creation summary:")
    print(f"Topics created: {topics_created}")
    print(f"Comments created: {comments_created}")


def populate():
    tags = populate_tags()
    users = create_users()
    forums = create_forums(users, tags)
    create_topics_and_comments(forums)

    print("\nPopulation completed successfully.")


if __name__ == '__main__':
    populate()
