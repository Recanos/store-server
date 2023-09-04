from django.db import models

# Create your models here.
class ProductsCategoty((models.Model)):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductsCategoty, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} | категория: {self.category.name}'