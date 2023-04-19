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
#   thumbnail = models.URLField()
#   images = models.ImageField()
#   price = models.DecimalField()

# class FavoritesList(models.Model):
#     comic = models.ManyToMany

# class Order(models.Model):
#      name = models.CharField()
#      is_gift = models.BooleanField()
#      gift_message = models.CharField(max_length=500)

# class Wishlist(models.Model):
#      user_id = models.IntegerField()