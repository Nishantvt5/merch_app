from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.customer_signup, name='signup'),
    path('login/', views.customer_login, name='login'),
    path('logout/', views.customer_logout, name='logout'),
]