# store/urls.py

from django.urls import path
from . import views

# Set the app namespace
app_name = 'store' 

urlpatterns = [
    # Home page - shows all products
    path('', views.product_list, name='product_list'),
    
    # Filtered view - shows products only in the selected category
    path('<slug:category_slug>/', views.product_list, name='product_filter'),
    
    # NEW: Product detail URL 
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]