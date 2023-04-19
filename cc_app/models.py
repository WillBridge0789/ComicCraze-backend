from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Comic(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=False)

# class FavoritesList(models.Model):
#     comic = ManyToMany
