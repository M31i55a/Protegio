import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress, EmailConfirmation

# Get the last created user
user = User.objects.latest('id')
print(f'✅ Last user created: {user.username}')
print(f'📧 Email: {user.email}')

# Get email address record
email_rec = EmailAddress.objects.get(user=user)
print(f'✅ EmailAddress record: verified={email_rec.verified}, primary={email_rec.primary}')

# Get the confirmation code
try:
    confirmation = EmailConfirmation.objects.filter(email_address=email_rec).latest('created')
    print(f'✅ Confirmation token created: {confirmation.created}')
    print(f'📝 Confirmation key (first 30 chars): {confirmation.key[:30]}...')
    print(f'\n📨 Verification URL would be:')
    print(f'   http://127.0.0.1:8000/accounts/confirm-email/{confirmation.key}/')
except Exception as e:
    print(f'ℹ️ No confirmation record yet: {e}')
