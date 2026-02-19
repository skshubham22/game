import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boardgames.settings')
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='admin')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"SUCCESS: User 'admin' is now a superuser (is_staff={user.is_staff}, is_superuser={user.is_superuser})")
except User.DoesNotExist:
    print("User 'admin' does not exist!")
