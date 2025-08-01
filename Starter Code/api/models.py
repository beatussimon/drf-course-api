from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="products", null=True, blank=True)

    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name 
    
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMEd = "Confirmed"
        CANCELED = "Canceled"

    products = models.ManyToManyField(Product, through="OrderItem")
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    status= models.CharField(
        max_length=10,
        choices = StatusChoices.choices,
        default= StatusChoices.PENDING
    )

    def __str__(self):
        return f"Order{self.order_id} by {self.user}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity