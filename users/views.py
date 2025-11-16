from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomerSignupForm




def customer_signup(request):
    """
    View for customer registration - uses CustomerSignupForm
    """
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auto-login after signup
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to our store.')
            return redirect('store:product_list')  # Adjust based on your store URL name
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerSignupForm()
    
    return render(request, 'users/signup.html', {'form': form})

def customer_login(request):
    """
    View for customer login
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_regular_customer():  # Only allow customers to login
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('store:product_list')  # Adjust based on your store URL name
            else:
                messages.error(request, 'This login is for customers only.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'users/login.html')

@login_required
def customer_logout(request):
    """
    View for customer logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('store:product_list')  # Adjust based on your store URL name

