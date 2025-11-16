# store/models.py

from django.db import models
from django.utils.text import slugify

## 1. Category Model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug from name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


## 2. Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug from name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)




## 3. Dynamic Attribute Models

# Defines the name of an attribute (e.g., "Color", "Size", "Material")
class ProductAttribute(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

# Stores the value of an attribute for a specific product
class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255) # e.g., "Red", "Large", "Cotton"

    class Meta:
        # Ensures a product can only have one value for a given attribute
        unique_together = ('product', 'attribute')
        verbose_name = 'Product Attribute Value'
        verbose_name_plural = 'Product Attribute Values'

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
    

class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d', 
        help_text='Upload a product image'
    )
    alt_text = models.CharField(
        max_length=255, 
        blank=True, 
        help_text='Descriptive text for the image (for accessibility/SEO)'
    )
    is_main = models.BooleanField(
        default=False, 
        help_text='Check if this is the main image for the product.'
    )
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['is_main', 'id'] # Main image first

    def __str__(self):
        return f"Image for {self.product.name}"