# create_initial_users.py
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meddy_tours.settings')
django.setup()

from django.contrib.auth.models import User, Group

def create_users():
    # Create content manager
    content_manager, created = User.objects.get_or_create(
        username='contentmanager',
        email='content@meddytours.com',
        defaults={
            'first_name': 'Content',
            'last_name': 'Manager',
            'is_staff': True
        }
    )

    if created:
        content_manager.set_password('securepassword123')
        content_manager.save()
        print("✓ Content manager user created")
    else:
        print("ℹ Content manager user already exists")

    # Assign to group
    try:
        content_group = Group.objects.get(name='Content_Managers')
        content_manager.groups.add(content_group)
        print("✓ Content manager added to group")
    except Group.DoesNotExist:
        print("✗ Content_Managers group not found. Run setup_groups first.")

    print("\nUser credentials:")
    print("Content Manager:")
    print("  Username: contentmanager")
    print("  Password: securepassword123")
    print("  URL: /content-manager/")

if __name__ == "__main__":
    create_users()