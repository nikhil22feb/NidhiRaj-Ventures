
from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='products/', blank=True, null=True)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name
