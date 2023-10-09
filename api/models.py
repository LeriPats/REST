from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class ApiUser(AbstractUser):
    user_types = (
        ('supplier', 'Поставщик'),
        ('consumer', 'Потребитель'),
        )
    user_type = models.CharField(max_length=10, choices=user_types)


class Store(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Item(models.Model):
    name = models.CharField(max_length=128)
    quantity = models.PositiveIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.store.name}. Item name: {self.name}"


class Order(models.Model):
    item = models.ForeignKey(Item, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(ApiUser, related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}; {self.item.store.name}; {self.item.name}"
