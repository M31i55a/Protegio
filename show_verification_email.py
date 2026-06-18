#!/usr/bin/env python
"""
Test script to display email verification link for the last registered user.
Run with: python manage.py shell < show_verification_email.py
"""

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress, EmailConfirmation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unified_tool.settings')
django.setup()

print("\n" + "="*70)
print("EMAIL VERIFICATION TEST")
print("="*70)

try:
    user = User.objects.latest('id')
    print(f'\n✅ Last user created: {user.username}')
    print(f'📧 Email: {user.email}')
    print(f'👤 User ID: {user.id}')

    email_rec = EmailAddress.objects.get(user=user)
    print(f'✅ EmailAddress verified: {email_rec.verified}')
    print(f'✅ EmailAddress primary: {email_rec.primary}')

    try:
        confirmation = EmailConfirmation.objects.filter(email_address=email_rec).latest('created')
        key = confirmation.key
        
        print(f'\n✅ Email confirmation created: {confirmation.created}')
        print(f'\n📝 VERIFICATION TOKEN:')
        print(f'   {key}')
        
        verify_url = f'http://127.0.0.1:8000/accounts/confirm-email/{key}/'
        print(f'\n📨 CLICK THIS LINK TO VERIFY EMAIL:')
        print(f'   {verify_url}')
        
        # Try to render the email template
        print(f'\n📧 EMAIL CONTENT PREVIEW:')
        print("-" * 70)
        try:
            from allauth.account.utils import user_logged_in
            from allauth.account.models import EmailConfirmation
            
            context = {
                'user': user,
                'activate_url': verify_url,
                'key': key,
                'expiration_days': settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS,
                'site_domain': 'http://127.0.0.1:8000',
            }
            
            # Try to load email templates
            from django.template import loader
            try:
                subject = loader.render_to_string('account/email/email_confirmation_subject.txt', context).strip()
                print(f"Subject: {subject}\n")
            except:
                print("Subject: [Template not found]\n")
            
            try:
                message = loader.render_to_string('account/email/email_confirmation_message.html', context)
                print("HTML Email Body (first 500 chars):")
                print(message[:500] + "...")
            except Exception as e:
                print(f"HTML Email: [Template error: {e}]")
                
        except Exception as e:
            print(f"Email rendering preview: {e}")
        
        print("-" * 70)
        
    except Exception as e:
        print(f'\n❌ No confirmation record yet: {e}')
        print("\nℹ️ Trying to send email confirmation...")
        from allauth.account.utils import send_email_confirmation
        try:
            send_email_confirmation(None, user)
            print("✅ Email confirmation sent!")
        except Exception as send_error:
            print(f"❌ Error sending email: {send_error}")

except User.DoesNotExist:
    print('❌ No users found in database')

print("\n" + "="*70 + "\n")
