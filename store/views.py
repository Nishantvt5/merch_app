from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, ProductAttribute, ProductAttributeValue, Cart, CartItem
from .forms import AddToCartForm

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


@login_required
def add_to_cart(request, product_id):
    """
    Add product to cart
    """
    product = get_object_or_404(Product, id=product_id, is_available=True)
    
    # Get or create cart for user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f'Updated {product.name} quantity in your cart.')
        else:
            messages.success(request, f'Added {product.name} to your cart.')
        
        return redirect('store:product_list')
    
    return redirect('store:product_list')

@login_required
def view_cart(request):
    """
    Display user's cart
    """
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('product').all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    context = {
        'shop_name': 'DD Creation',
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)

@login_required
def update_cart_item(request, item_id):
    """
    Update cart item quantity
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    
    return redirect('store:view_cart')

@login_required
def remove_from_cart(request, item_id):
    """
    Remove item from cart
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from your cart.')
    
    return redirect('store:view_cart')