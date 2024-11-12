from django.db import models

# Create your models here.

class Stock(models.Model):
    stock = models.CharField(max_length=100)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stock