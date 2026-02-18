import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boardgames.settings')
django.setup()

from django.contrib.auth.models import User

user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
if created:
    print("Created new superuser 'admin'")
else:
    print("Found existing superuser 'admin'")

user.set_password('admin')
user.save()
print("Password for 'admin' has been set to 'admin'")
