# store/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductAttribute, ProductAttributeValue, ProductImage, Cart, CartItem

# --- Inline for Dynamic Attributes ---
class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1

# --- Inline for Images ---
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5

# --- Inline for Cart Items ---
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product_details', 'quantity', 'unit_price', 'total_price_display']
    fields = ['product_details', 'quantity', 'unit_price', 'total_price_display']
    
    def product_details(self, obj):
        if obj.product:
            # Get the main product image
            main_image = obj.product.images.filter(is_main=True).first()
            image_html = ""
            if main_image:
                image_html = f'<img src="{main_image.image.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px; margin-right: 10px;" alt="{obj.product.name}">'
            
            product_info = f"""
            <div style="display: flex; align-items: center;">
                {image_html}
                <div>
                    <strong>{obj.product.name}</strong><br>
                    <small>Category: {obj.product.category.name}</small><br>
                    <small>Stock: {obj.product.stock}</small>
                </div>
            </div>
            """
            return format_html(product_info)
        return "No Product"
    product_details.short_description = 'Product Details'
    
    def unit_price(self, obj):
        return f"Rs. {obj.product.price}"
    unit_price.short_description = 'Unit Price'
    
    def total_price_display(self, obj):
        return f"<strong>Rs. {obj.total_price}</strong>"
    total_price_display.short_description = 'Total Price'
    total_price_display.allow_tags = True

# --- Category Admin (CORRECTED) ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'product_count']
    list_filter = ['is_active']
    search_fields = ['name']
    # REMOVED prepopulated_fields since slug is non-editable
    fields = ('name', 'description', 'is_active')  # REMOVED slug from here
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

# --- Product Admin (CORRECTED) ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_available']
    # REMOVED prepopulated_fields since slug is non-editable
    inlines = [ProductImageInline, ProductAttributeValueInline]
    fields = ('name', 'category', 'description', 'price', 'stock', 'is_available')  # REMOVED slug from here

# --- Product Attribute Admin ---
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'values_count']
    search_fields = ['name']
    
    def values_count(self, obj):
        return obj.productattributevalue_set.count()
    values_count.short_description = 'Values Count'

# --- Product Attribute Value Admin ---
@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['product', 'attribute', 'value']
    list_filter = ['attribute', 'product__category']
    search_fields = ['product__name', 'value']

# --- Cart Admin ---
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'user_name', 'items_count', 'total_quantity', 'total_price_display', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at', 'total_price_display', 'total_quantity_display', 'items_list']
    inlines = [CartItemInline]
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'
    
    def user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or "No Name"
    user_name.short_description = 'Name'
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items Count'
    
    def total_price_display(self, obj):
        return f"<strong style='color: green;'>Rs. {obj.total_price}</strong>"
    total_price_display.short_description = 'Total Value'
    total_price_display.allow_tags = True
    
    def total_quantity_display(self, obj):
        return obj.total_quantity
    total_quantity_display.short_description = 'Total Items'
    
    def items_list(self, obj):
        """Display all items in the cart in the detail view"""
        items = obj.items.select_related('product', 'product__category').all()
        if not items:
            return "No items in cart"
        
        items_html = "<div style='max-height: 300px; overflow-y: auto;'>"
        for item in items:
            main_image = item.product.images.filter(is_main=True).first()
            image_html = ""
            if main_image:
                image_html = f'<img src="{main_image.image.url}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px; margin-right: 10px;" alt="{item.product.name}">'
            
            items_html += f"""
            <div style="display: flex; align-items: center; padding: 8px; border-bottom: 1px solid #eee;">
                {image_html}
                <div style="flex: 1;">
                    <strong>{item.product.name}</strong><br>
                    <small>Category: {item.product.category.name} | Price: Rs. {item.product.price}</small>
                </div>
                <div style="text-align: right;">
                    <strong>Qty: {item.quantity}</strong><br>
                    <strong style="color: green;">Rs. {item.total_price}</strong>
                </div>
            </div>
            """
        items_html += "</div>"
        return format_html(items_html)
    items_list.short_description = 'Cart Items Preview'
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'user_name', 'user_email')
        }),
        ('Cart Summary', {
            'fields': ('total_quantity_display', 'total_price_display', 'items_list')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# --- CartItem Admin ---
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart_user', 'product_with_image', 'category', 'unit_price', 'quantity', 'total_price_display', 'stock_status']
    list_filter = ['cart__user', 'product__category', 'product__is_available']
    search_fields = ['cart__user__email', 'product__name', 'product__category__name']
    readonly_fields = ['product_details', 'unit_price_display', 'total_price_display', 'stock_status']
    
    def cart_user(self, obj):
        return obj.cart.user.email
    cart_user.short_description = 'Customer'
    cart_user.admin_order_field = 'cart__user__email'
    
    def product_with_image(self, obj):
        main_image = obj.product.images.filter(is_main=True).first()
        if main_image:
            return format_html(
                '<img src="{}" style="width: 30px; height: 30px; object-fit: cover; border-radius: 4px; margin-right: 8px;" alt="{}"> {}',
                main_image.image.url,
                obj.product.name,
                obj.product.name
            )
        return obj.product.name
    product_with_image.short_description = 'Product'
    product_with_image.admin_order_field = 'product__name'
    
    def category(self, obj):
        return obj.product.category.name
    category.short_description = 'Category'
    category.admin_order_field = 'product__category__name'
    
    def unit_price(self, obj):
        return f"Rs. {obj.product.price}"
    unit_price.short_description = 'Unit Price'
    
    def total_price_display(self, obj):
        return f"<strong style='color: green;'>Rs. {obj.total_price}</strong>"
    total_price_display.short_description = 'Total Price'
    total_price_display.allow_tags = True
    
    def stock_status(self, obj):
        if obj.product.stock >= obj.quantity:
            return format_html('<span style="color: green;">✓ Adequate ({})</span>', obj.product.stock)
        else:
            return format_html('<span style="color: red;">✗ Low Stock ({})</span>', obj.product.stock)
    stock_status.short_description = 'Stock Status'
    
    def product_details(self, obj):
        """Detailed product information for the detail view"""
        main_image = obj.product.images.filter(is_main=True).first()
        image_html = ""
        if main_image:
            image_html = f'<img src="{main_image.image.url}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px; margin-right: 15px;" alt="{obj.product.name}">'
        
        product_info = f"""
        <div style="display: flex; align-items: start; margin-bottom: 20px;">
            {image_html}
            <div>
                <h4>{obj.product.name}</h4>
                <p><strong>Category:</strong> {obj.product.category.name}</p>
                <p><strong>Description:</strong> {obj.product.description[:100]}...</p>
                <p><strong>Price:</strong> Rs. {obj.product.price}</p>
                <p><strong>Stock Available:</strong> {obj.product.stock}</p>
                <p><strong>Available:</strong> {'Yes' if obj.product.is_available else 'No'}</p>
            </div>
        </div>
        """
        return format_html(product_info)
    product_details.short_description = 'Product Information'
    
    def unit_price_display(self, obj):
        return f"Rs. {obj.product.price}"
    unit_price_display.short_description = 'Unit Price'
    
    fieldsets = (
        ('Product Information', {
            'fields': ('product_details',)
        }),
        ('Cart Information', {
            'fields': ('cart', 'quantity')
        }),
        ('Pricing', {
            'fields': ('unit_price_display', 'total_price_display')
        }),
        ('Inventory', {
            'fields': ('stock_status',)
        }),
    )