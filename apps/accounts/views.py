from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.signals import email_confirmed
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import datetime

# ============ AUTHENTICATION VIEWS ============

@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view with Remember Me support"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # "Remember Me" logic
            if not remember_me:
                # Session expires when browser closes
                request.session.set_expiry(0)
            else:
                # Session lasts 2 weeks (Django default)
                request.session.set_expiry(1209600)
            
            next_page = request.GET.get('next', 'dashboard:home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')


@require_http_methods(["GET", "POST"])
def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('accounts:signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('accounts:signup')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create EmailAddress for allauth (required for email verification)
        email_address = EmailAddress.objects.create(
            user=user,
            email=email,
            verified=False,  # Requires email verification
            primary=True
        )
        
        # Create EmailConfirmation record
        confirmation = EmailConfirmation.create(email_address)
        
        # Send verification email manually
        try:
            send_verification_email(request, user, confirmation)
        except Exception as e:
            print(f"Email send error: {e}")
        
        # Login with explicit backend (needed when multiple backends exist)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        messages.success(request, 'Registration successful! Please check your email to verify your account.')
        return redirect('account_email_verification_sent')
    
    return render(request, 'accounts/signup.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('accounts:login')


# ============ USER PROFILE VIEWS ============

@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def activity_log_view(request):
    """User activity log view"""
    return render(request, 'accounts/activity.html')


@login_required
def scan_history_view(request):
    """User scan history view"""
    return render(request, 'accounts/scans.html')


# ============ ADMIN VIEWS ============

@login_required
def admin_users_view(request):
    """Admin users management view"""
    if not request.user.is_staff:
        return redirect('dashboard:dashboard')
    
    users = User.objects.all()
    return render(request, 'accounts/admin_users.html', {'users': users})


@login_required
def admin_audit_log_view(request):
    """Admin audit log view"""
    if not request.user.is_staff:
        return redirect('dashboard:dashboard')
    
    return render(request, 'accounts/admin_audit.html')


# ============ API VIEWS ============

@login_required
def get_audit_stats_api(request):
    """Get audit statistics (API endpoint)"""
    from django.http import JsonResponse
    
    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
    }
    
    return JsonResponse(stats)


# ============ HELPER FUNCTIONS ============

def send_verification_email(request, user, confirmation):
    """Send email verification email"""
    try:
        # Build verification URL
        verify_url = request.build_absolute_uri(
            f'/accounts/confirm-email/{confirmation.key}/'
        )
        
        # Email context
        context = {
            'user': user,
            'email': user.email,
            'activate_url': verify_url,
            'key': confirmation.key,
            'expiration_days': settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS,
            'site_domain': request.build_absolute_uri('/').rstrip('/'),
        }
        
        # Render email subject and body
        subject = 'PROTEGIO - Verify Your Email Address'
        
        # Try HTML email first
        try:
            html_message = render_to_string('account/email/email_confirmation_message.html', context)
        except:
            html_message = f'''
            <p>Hello {user.email},</p>
            <p>Thank you for signing up with PROTEGIO!</p>
            <p><a href="{verify_url}">Click here to verify your email</a></p>
            <p>This link will expire in {settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS} days.</p>
            '''
        
        # Send email
        send_mail(
            subject=subject,
            message=f'Visit this link to verify your email: {verify_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"✅ Verification email sent to {user.email}")
        
    except Exception as e:
        print(f"❌ Error sending verification email: {e}")
        raise
