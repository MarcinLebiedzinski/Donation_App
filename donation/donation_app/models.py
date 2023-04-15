from django.db import models
from django.contrib.auth.models import User


TYPE_CHOICES = [
    (-1, "not defined"),
    (0, "fundacja"),
    (1, "organizacja pozarządowa"),
    (2, "zbiórka lokalna")
]


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    day_name = models.SmallIntegerField(choices=TYPE_CHOICES, default=0, null=False)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.PositiveSmallIntegerField(null=True)
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64) #docelowo do zmiany na specjalny (instalacja)
    phone_number = models.CharField(max_length=64) #docelowo do zmiany na specjalny (instalacja)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6) #docelowo do zmiany na specjalny (instalacja)
    pick_up_date = models.DateField(null=False)
    pick_up_time = models.TimeField(null=False)
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE) # jak zdefiniować default null



