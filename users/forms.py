# users/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users. Includes all required fields.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'is_admin') # Added is_admin for admin registration
        
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
    A form for updating existing users.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_customer')