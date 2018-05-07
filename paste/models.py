from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils import timezone
from datetime import datetime, timedelta
from webtools import settings
from django.utils.translation import ugettext_lazy as _
import hashlib
import uuid


EXPIRE_CHOICES = (
    (0, _('Never expire')),
    (60, _('1 hour')),
    (60 * 24, _('1 day')),
    (60 * 24 * 7, _('1 week')),
    (60 * 24 * 7 * 30, _('1 month')),
    (60 * 24 * 7 * 365, _('1 year')),
)


class Language(models.Model):
    """Language object."""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __unicode__(self):
        """String representation."""
        return _(self.name)

    def __str__(self):
        return str(_(self.name))


class Paste(models.Model):
    """Paste object."""
    language = models.ForeignKey(Language, default=14, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, editable=False)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(validators=[MaxLengthValidator(
        settings.PASTE['max_characters'])])
    size = models.IntegerField(default=0, editable=False)
    paste_time = models.DateTimeField(default=datetime.now, editable=False)
    paste_ip = models.GenericIPAddressField(editable=False)
    paste_agent = models.CharField(max_length=200, editable=False)
    lifetime = models.IntegerField(default=settings.PASTE['default_lifetime'],
                                   choices=EXPIRE_CHOICES)
    lifecount = models.IntegerField(default=0, blank=True)
    viewcount = models.IntegerField(default=0, editable=False)
    expired = models.BooleanField(default=False, editable=False)
    private = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True)
    salt = models.CharField(max_length=36, blank=True)

    def compute_size(self):
        """Computes size."""
        self.size = len(self.content)

    def is_expired(self):
        """Return expiration status."""
        if self.expired or self.time_expired() or self.view_expired():
            return True
        return False

    def time_expired(self):
        """Check if paste lifetime is over."""
        if not self.lifetime or self.lifetime - self.get_age() > 0:
            return False
        self.mark_expired()
        return True

    def get_age(self):
        """Return age in minutes"""
        delta = timezone.now() - self.paste_time
        return divmod(delta.days * 86400 + delta.seconds, 60)[0]

    def expiration_time(self):
        """Return expiration time"""
        if not self.lifetime:
            return None
        delta = timedelta(minutes=self.lifetime)
        return self.paste_time + delta

    def mark_expired(self):
        """Mark paste expired."""
        self.expired = True
        self.save()

    def incr_viewcount(self):
        """Increment view counter."""
        self.viewcount = self.viewcount + 1
        self.save()

    def view_expired(self):
        """Check if paste view count is over."""
        if not self.lifecount:
            return False
        if self.lifecount <= self.viewcount:
            self.mark_expired()
            return True
        return False

    def _hash(self, raw):
        """Return hashed string."""
        if not self.salt:
            self.salt = str(uuid.uuid1())
        return hashlib.sha512((raw+self.salt).encode()).hexdigest()

    def set_password(self, raw):
        """Define a hashed password."""
        self.password = self._hash(raw)

    def pwd_match(self, password):
        """Compare provided password to paste's one."""
        if not password or not self._hash(password) == self.password:
            return False
        return True

    def __unicode__(self):
        """String representation."""
        return self.slug
