from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line
import os

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "regress_fast.settings")

# Get the User model
User = get_user_model()

# Get admin user and change password
admin = User.objects.get(username='admin')
admin.set_password('123456')
admin.save()

print("Admin password has been changed to 123456")
