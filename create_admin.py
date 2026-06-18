#!/usr/bin/env python
"""Create admin user if it doesn't exist"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✓ Superuser admin created')
else:
    print('✓ Superuser admin already exists')

# Create test users
test_users = [
    ('user1', 'user1@example.com', 'password123'),
    ('user2', 'user2@example.com', 'password123'),
]

for username, email, password in test_users:
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username, email, password)
        print(f'✓ User {username} created')
    else:
        print(f'✓ User {username} already exists')

print('\n✅ User setup completed!')
