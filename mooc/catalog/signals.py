from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from django.conf import settings
from pinax.badges.registry import badges

from .models import Profile, User
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# post_save.connect(create_user_profile, sender=User)

# @receiver('edit_profile')
# def edit_profile_points(payload):
#     user_id = payload['user_id']
#     user = User.objects.get(id=user_id)
#     cur_user = Profile.objects.get(user=user)
#     award_points(cur_user,20)