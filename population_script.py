import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatterchums.settings')
django.setup()

from forums.models import Tag


def populate_tags():
    tags = [
        # General Categories
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


if __name__ == '__main__':
    print("Starting ChatterChums tag population script...")
    populate_tags()