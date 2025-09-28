# meddy_tourguides/management/commands/create_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from meddy_tourguides.models import Destination, BlogPost, TeamMember, Testimonial

class Command(BaseCommand):
    help = 'Create initial users with different roles for Meddy Tours'

    def handle(self, *args, **options):
        # Create content manager user
        try:
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
                self.stdout.write(self.style.SUCCESS('Content manager user created'))
            else:
                self.stdout.write(self.style.WARNING('Content manager user already exists'))
            
            # Assign to content managers group
            try:
                content_group = Group.objects.get(name='Content_Managers')
                content_manager.groups.add(content_group)
                self.stdout.write(self.style.SUCCESS('Content manager added to group'))
            except Group.DoesNotExist:
                self.stdout.write(self.style.ERROR('Content_Managers group does not exist. Run setup_groups first.'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))

        self.stdout.write(self.style.SUCCESS('User creation process completed'))