from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import os.path
from django.contrib.auth.models import User

from django.db.models.signals import post_save

def get_image_path(instance, filename):
    return os.path.join('avatars', str(instance.id), filename)
# Create your models here.
@python_2_unicode_compatible
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.

    location = models.CharField(max_length=140, blank=True)
    gender = models.CharField(max_length=140, blank=True)
    age = models.IntegerField(default=0, blank=True)
    company = models.CharField(max_length=50, blank=True)

    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to=get_image_path, blank=True)

    # Override the __str__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

# Signal while saving user
post_save.connect(create_profile, sender=User)
