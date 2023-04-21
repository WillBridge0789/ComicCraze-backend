from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # favorites_list = models.ForeignKey('FavoritesList', on_delete=models.PROTECT, null=True)
    # wishlist = models.ForeignKey('Wishlist', on_delete=models.PROTECT, null=True)
    # items = models.ForeignKey('Items', on_delete=models.PROTECT, null=True)
    pass

    def __str__(self):
        return self.username

class Comic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    thumbnail = models.URLField(null=True)
#   images = models.ImageField()
    # price = models.DecimalField()

class FavoritesList(models.Model):
    comic = models.ManyToManyField('Comic')

# class Items(models.Model):
#      name = models.CharField()
#      is_gift = models.BooleanField()
#      gift_message = models.CharField(max_length=500)

# class Wishlist(models.Model):
#      user_id = models.IntegerField()