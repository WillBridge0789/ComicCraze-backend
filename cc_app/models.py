from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    favorite_comics = models.ManyToManyField('Comic', related_name="users")
    wishlist = models.ForeignKey('Wishlist', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.username

class Comic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    thumbnail = models.URLField(null=True)
#   images = models.ImageField()
#   price = models.DecimalField()

class Order(models.Model):
    is_gift = models.BooleanField()
    gift_message = models.CharField(max_length=500)
    item = models.ManyToManyField('Comic', related_name="cart_item")
    purchaser = models.ForeignKey('CustomUser', on_delete=models.PROTECT, null=True)

class Wishlist(models.Model):
    user_id = models.IntegerField()