# store/urls.py

from django.urls import path
from . import views

# Set the app namespace
app_name = 'store' 

urlpatterns = [
    # Home page - shows all products
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('', views.product_list, name='product_list'),
    
    # Filtered view - shows products only in the selected category
    path('<slug:category_slug>/', views.product_list, name='product_filter'),
    
    # NEW: Product detail URL 
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),

]