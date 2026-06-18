from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress, EmailConfirmation


class Command(BaseCommand):
    help = 'Display email verification link for the last registered user'

    def handle(self, *args, **options):
        try:
            user = User.objects.latest('id')
            self.stdout.write(f'\n✅ Last user created: {user.username}')
            self.stdout.write(f'📧 Email: {user.email}')

            email_rec = EmailAddress.objects.get(user=user)
            self.stdout.write(f'✅ EmailAddress: verified={email_rec.verified}, primary={email_rec.primary}')

            try:
                confirmation = EmailConfirmation.objects.filter(email_address=email_rec).latest('created')
                key = confirmation.key
                self.stdout.write(f'\n✅ Verification token created: {confirmation.created}')
                self.stdout.write(f'📝 Token: {key}\n')
                self.stdout.write(f'📨 Verification URL:')
                self.stdout.write(f'   http://127.0.0.1:8000/accounts/confirm-email/{key}/\n')
            except Exception as e:
                self.stdout.write(f'ℹ️ No confirmation record yet: {e}\n')

        except User.DoesNotExist:
            self.stdout.write('❌ No users found')
