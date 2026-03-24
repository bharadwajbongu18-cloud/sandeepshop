from django.db import models

class Claim(models.Model):
    username = models.CharField(max_length=100, unique=True)
    profile_link = models.URLField()
    claimed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username