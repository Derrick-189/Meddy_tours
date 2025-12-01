# meddy_tourguides/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from meddy_tourguides.models import Destination, BlogPost, TeamMember, Testimonial

class Command(BaseCommand):
    help = 'Creates user groups, permissions, and initial users for Meddy Tours'

    def handle(self, *args, **options):
        self.setup_groups()
        self.create_users()
        
    def setup_groups(self):
        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Website_Admins')
        content_group, created = Group.objects.get_or_create(name='Content_Managers')
        
        # Get content types and permissions (your existing code)
        destination_ct = ContentType.objects.get_for_model(Destination)
        blogpost_ct = ContentType.objects.get_for_model(BlogPost)
        teammember_ct = ContentType.objects.get_for_model(TeamMember)
        testimonial_ct = ContentType.objects.get_for_model(Testimonial)
        
        # ... rest of your group setup code ...
        
        self.stdout.write(self.style.SUCCESS('✓ Groups and permissions setup completed'))
    
    def create_users(self):
        # Create content manager user
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
            self.stdout.write(self.style.SUCCESS('✓ Content manager user created'))
        else:
            self.stdout.write(self.style.WARNING('ℹ Content manager user already exists'))

        # Assign to content managers group
        try:
            content_group = Group.objects.get(name='Content_Managers')
            content_manager.groups.add(content_group)
            self.stdout.write(self.style.SUCCESS('✓ Content manager added to group'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('✗ Content_Managers group not found'))

        # Display login information
        self.stdout.write(self.style.SUCCESS('\nUser credentials created:'))
        self.stdout.write(self.style.SUCCESS('Content Manager:'))
        self.stdout.write(self.style.SUCCESS('  Username: contentmanager'))
        self.stdout.write(self.style.SUCCESS('  Password: securepassword123'))
        self.stdout.write(self.style.SUCCESS('  Admin URL: /content-manager/'))