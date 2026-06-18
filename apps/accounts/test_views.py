from django.shortcuts import render
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress, EmailConfirmation


def test_email_verification_view(request):
    """Test view to display email verification links"""
    context = {'users': []}
    
    try:
        users = User.objects.all().order_by('-id')[:5]
        
        for user in users:
            user_data = {
                'username': user.username,
                'email': user.email,
                'email_address': None,
                'confirmation': None,
                'verify_url': None,
            }
            
            try:
                email_rec = EmailAddress.objects.get(user=user)
                user_data['email_address'] = {
                    'email': email_rec.email,
                    'verified': email_rec.verified,
                    'primary': email_rec.primary,
                }
                
                try:
                    confirmation = EmailConfirmation.objects.filter(email_address=email_rec).latest('created')
                    user_data['confirmation'] = {
                        'key': confirmation.key,
                        'created': confirmation.created,
                    }
                    user_data['verify_url'] = f'/accounts/confirm-email/{confirmation.key}/'
                except:
                    pass
            except:
                pass
            
            context['users'].append(user_data)
    except:
        pass
    
    return render(request, 'test_email_verification.html', context)
