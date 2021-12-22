from django.utils import timezone
from django.db import models
from django.utils.crypto import get_random_string


class URLToken(models.Model):

    token = models.CharField(max_length=256,
                             blank=True,
                             primary_key=True)
    user = models.ForeignKey(to='users.User', related_name='url_tokens', on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        """
        Update timestamps on save
        :return:
        """
        if not self.token:
            self.created = timezone.now()
        self.token = get_random_string(40)
        self.updated = timezone.now()
        return super(URLToken, self).save(*args, **kwargs)

