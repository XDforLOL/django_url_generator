from datetime import datetime, timedelta
from django.db import models

#TODO: Rename this to Urls
# should've been called URLS
class Url(models.Model):
    short_endpoint = models.CharField(max_length=6, unique=True, null=False)
    long_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # I gave each one of the urls an expiration date of 30 days
    expiration_date = models.DateTimeField(null=True, blank=True, default=datetime.now()+timedelta(days=30))

    def __str__(self):
        return self.long_url

class Redirect(models.Model):
    # I am using the url
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    # simple redirect count
    redirect_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('url', 'ip_address', 'user_agent')

    def __str__(self):
        return f"{self.url} - {self.ip_address} - {self.user_agent}"