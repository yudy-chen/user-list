from django.db import models

class User(models.Model):
    
    user_name = models.CharField(max_length=255)

    age = models.IntegerField()
    
    photo_path = models.CharField(max_length=255, default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)