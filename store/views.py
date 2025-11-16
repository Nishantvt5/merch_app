from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductAttribute, ProductAttributeValue

def product_list(request, category_slug=None):
    """
    Renders the main product listing page, optionally filtered by category.
    """
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_available=True)
    
    current_category = None
    
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    context = {
        'shop_name': 'DD Creation',
        'current_category': current_category,
        'categories': categories,
        'products': products.select_related('category').prefetch_related('images'), 
    }
    
    return render(request, 'store/product_list.html', context)

def product_detail(request, category_slug, product_slug):
    """
    Renders the single product detail page.
    """
    # Fetch the product based on its slug and category slug for a clean URL structure
    product = get_object_or_404(
        Product.objects.prefetch_related('attribute_values__attribute', 'images'),
        slug=product_slug, 
        category__slug=category_slug,
        is_available=True
    )

    # Separate images for easy rendering (main image vs. gallery)
    main_image = product.images.filter(is_main=True).first()
    gallery_images = product.images.all().exclude(pk=main_image.pk) if main_image else product.images.all()

    # Dynamic Attributes
    attributes = product.attribute_values.all()
    
    context = {
        'shop_name': 'DD Creation',
        'product': product,
        'main_image': main_image,
        'gallery_images': gallery_images,
        'attributes': attributes,
    }

    return render(request, 'store/product_detail.html', context)