from __future__ import unicode_literals
from django.contrib.auth.admin import User
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib
import os
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver


class UploadFile(models.Model):
    """Uploadfile and save."""

    file = models.ImageField(upload_to='profile/%Y/%m/%d')
    owner = models.ForeignKey(User)
    edited = models.SmallIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    thumbnail = ImageSpecField(source='file',
                                      processors=[ResizeToFill(120, 120)],
                                      format='JPEG',
                                      options={'quality': 100})

    class Meta:
        ordering = ('-modified_on',)


class UserProfile(models.Model):
    """Add a picture to users"""

    user = models.OneToOneField(User, related_name='profile')

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(
            user_id=self.user.id, provider='facebook')
        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


def _delete_file(path):
    """Deletes file from filesystem."""
    if os.path.isfile(path):
        os.remove(path)


@receiver(models.signals.pre_delete, sender=UploadFile)
def delete_file(sender, instance, *args, **kwargs):
    """Delete image fils on `post_delete`."""
    if instance.file:
        _delete_file(instance.file.path)


@receiver(models.signals.pre_delete, sender=UploadFile)
def delete_thumbnail(sender, instance, *args, **kwargs):
    """Delete thumbnail files on `post_delete`."""
    if instance.thumbnail:
        _delete_file(instance.thumbnail.path)
