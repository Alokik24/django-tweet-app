from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Tweet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField(max_length=240)
    photo=models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(blank=True, null=True)
    is_flagged = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old = Tweet.objects.get(pk=self.pk)
            if old.text != self.text or old.photo != self.photo:
                self.edited_at = timezone.now()
            else:
                self.edited_at = old.edited_at
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.username} {self.text[:10]}"
