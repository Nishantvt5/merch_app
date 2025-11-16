from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomerSignupForm(UserCreationForm):
    """
    A form for creating new CUSTOMER users only.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Force all users created with this form to be customers
        user.is_customer = True
        user.is_admin = False
        user.is_staff = False
        
        if commit:
            user.save()
        return user


class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users in ADMIN interface only.
    This should only be used in Django admin.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'is_admin')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        # If is_admin is checked, set is_customer to False and is_staff to True
        if user.is_admin:
            user.is_customer = False
            user.is_staff = True
        else:
            # Default new user is a customer
            user.is_customer = True
            user.is_admin = False
            user.is_staff = False
            
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating existing users in ADMIN interface.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_customer')