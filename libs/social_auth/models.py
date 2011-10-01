"""Social auth models"""
from datetime import timedelta

from django.db import models
from django.conf import settings

from social_auth.fields import JSONField

# If User class is overridden, it *must* provide the following fields
# and methods work with django-social-auth:
#
#   username   = CharField()
#   last_login = DateTimeField()
#   is_active  = BooleanField()
#   def is_authenticated():
#       ...

if getattr(settings, 'SOCIAL_AUTH_USER_MODEL', None):
    User = models.get_model(*settings.SOCIAL_AUTH_USER_MODEL.rsplit('.', 1))
else:
    from django.contrib.auth.models import User


class UserSocialAuth(models.Model):
    """Social Auth association model"""
    user = models.ForeignKey(User, related_name='social_auth')
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = JSONField(blank=True)

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')

    def __unicode__(self):
        """Return associated user unicode representation"""
        return unicode(self.user)

    def expiration_delta(self):
        """Return saved session expiration seconds if any. Is retuned in
        the form of a timedelta data type. None is returned if there's no
        value stored or it's malformed.
        """
        if self.extra_data:
            name = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')
            try:
                return timedelta(seconds=int(self.extra_data.get(name)))
            except (ValueError, TypeError):
                pass
        return None

    @property
    def oauth_token_secret(self):
        parameters = self.extra_data.get('access_token')
        oauth_token_secret = parameters.split('&')[0]
        oauth_token_secret = oauth_token_secret.split('=').pop()
        return oauth_token_secret

    @property
    def oauth_token(self):
        parameters = self.extra_data.get('access_token')
        oauth_token = parameters.split('&')[1]
        oauth_token = oauth_token.split('=').pop()
        return oauth_token

class Nonce(models.Model):
    """One use numbers"""
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    def __unicode__(self):
        """Unicode representation"""
        return self.server_url


class Association(models.Model):
    """OpenId account association"""
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)  # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    def __unicode__(self):
        """Unicode representation"""
        return '%s %s' % (self.handle, self.issued)
