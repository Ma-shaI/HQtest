from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ProductAccess(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
