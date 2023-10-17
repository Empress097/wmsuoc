from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    
    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Food Title")
    slug = models.SlugField(max_length=160, verbose_name="Food Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Food ID (SKU)")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Product Category", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?")
    food_image = models.ImageField(upload_to='food', blank=True, null=True, verbose_name="Food Image")
    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Foodlist", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)
    
    @property
    def total_price(self):
        return self.quantity * self.product.price
    
class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)
    store_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.store_name