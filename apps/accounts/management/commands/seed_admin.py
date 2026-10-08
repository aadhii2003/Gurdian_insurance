from django.core.management.base import BaseCommand
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Seeds the admin user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            user = User(
                username='admin',
                email='admin@gmail.com',
                full_name='Admin'
            )
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully seeded admin user'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
