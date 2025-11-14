"""
Management command to create initial admin user
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from employee.models import Employee


class Command(BaseCommand):
    help = 'Creates initial admin user and employee record'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if admin already exists
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists'))
            return
        
        try:
            # Create superuser
            user = User.objects.create_superuser(
                username='admin',
                email='admin@horilla.com',
                password='admin123'
            )
            
            # Create employee
            employee = Employee()
            employee.employee_user_id = user
            employee.badge_id = 'EMP001'
            employee.employee_first_name = 'Admin'
            employee.employee_last_name = 'User'
            employee.email = 'admin@horilla.com'
            employee.phone = '+1234567890'
            employee.save()
            
            self.stdout.write(self.style.SUCCESS('Successfully created admin user!'))
            self.stdout.write(self.style.SUCCESS('Username: admin'))
            self.stdout.write(self.style.SUCCESS('Password: admin123'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating admin: {str(e)}'))
