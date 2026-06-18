from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

# Create a test user
user = User.objects.create_user(
    username='john.doe',
    email='john.doe@example.com',
    password='testpass123'
)

# Create email address for allauth (mandatory for email-only login)
email = EmailAddress.objects.create(
    user=user,
    email='john.doe@example.com',
    verified=False,  # Not verified yet
    primary=True
)

print(f"✅ User created: {user.username}")
print(f"✅ Email: {user.email}")
print(f"✅ EmailAddress verified: {email.verified}")
print(f"✅ EmailAddress primary: {email.primary}")
