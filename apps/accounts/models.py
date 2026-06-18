from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

ACCOUNT_TYPES = [
    ('google', 'Google'),
    ('microsoft', 'Microsoft'),
    ('github', 'GitHub'),
    ('manual', 'Email/Password'),
]


class UserProfile(models.Model):
    """Extended user profile to track account type and settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
        default='manual',
        help_text='Type de compte utilisé pour l\'authentification'
    )
    avatar_url = models.URLField(
        blank=True,
        null=True,
        help_text='Avatar URL from social provider'
    )
    bio = models.TextField(blank=True, help_text='User bio')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_account_type_display()}"
    
    @property
    def social_accounts(self):
        """Get all connected social accounts"""
        from allauth.socialaccount.models import SocialAccount
        return SocialAccount.objects.filter(user=self.user)
    
    def has_social_account(self, provider):
        """Check if user has a specific social account connected"""
        from allauth.socialaccount.models import SocialAccount
        return SocialAccount.objects.filter(user=self.user, provider=provider).exists()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile whenever a new User is created"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile whenever the User is saved"""
    try:
        instance.profile.save()
    except:
        pass

