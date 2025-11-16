# store/admin.py

from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductAttributeValue, ProductImage

# --- 1. Inline for Dynamic Attributes ---
class ProductAttributeValueInline(admin.TabularInline):
    """Allows adding/editing attributes directly on the Product page."""
    model = ProductAttributeValue
    extra = 1

# --- 1.2 Inline for Images (NEW) ---
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # Start with 1 empty slot
    max_num = 5 # Limit the total number of images to 5


# --- 2. Category Admin ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Handles Category management. 
    The 'slug' field is excluded from the form because it is auto-generated in the model's save method.
    """
    list_display = ('name', 'is_active', 'slug')
    search_fields = ('name',)
    
    # FIX: Explicitly list only the editable fields. 
    # Since slug is not editable, we must not include it or use prepopulated_fields.
    fields = ('name', 'description', 'is_active') 

# --- 3. Product Attribute Admin ---
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """
    Handles Attribute definition (e.g., 'Color', 'Size').
    """
    list_display = ('name',)
    search_fields = ('name',)


# --- 4. Product Admin ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ['price', 'stock', 'is_available']
    
    # 🎯 UPDATED: Include both Inlines
    inlines = [ProductAttributeValueInline, ProductImageInline] 
    
    # We use a custom fields tuple for the form, excluding 'slug' for auto-generation.
    fields = (
        'name', 
        'category', 
        'description', 
        'price', 
        'stock', 
        'is_available'
    )