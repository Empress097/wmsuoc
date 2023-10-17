from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError
from wmsuoc.models import *

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'auto-focus':True, 'class':'form-control', 'placeholder':'Current Password'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'Confirm Password'}))

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
    
class UsersCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '\uf054 First Name', 'style': 'font-family: Arial, FontAwesome;'}))
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '\uf054 Last Name', 'style': 'font-family: Arial, FontAwesome;'}))
    middle_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '\uf054 Middle Initial', 'style': 'font-family: Arial, FontAwesome;'}))
    contact_number = forms.CharField(max_length=20, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '\uf054 Contact', 'style': 'font-family: Arial, FontAwesome;'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': '\uf054 Email', 'style': 'font-family: Arial, FontAwesome;'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '\uf054 Username', 'style': 'font-family: Arial, FontAwesome;'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': '\uf054 Password', 'style': 'font-family: Arial, FontAwesome;'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': '\uf054 Retype Password', 'style': 'font-family: Arial, FontAwesome;'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@wmsu.edu.ph'):
            raise forms.ValidationError('Email must end with @wmsu.edu.ph')
        return email
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'contact_number', 'email', 'password1', 'password2')
    
class VendorCreationForm(forms.Form):
    store_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Store Name'}))
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter First Name'}))
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Last Name'}))
    middle_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Middle Name'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter Email Address'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Username'}))
    contact_number = forms.CharField(max_length=20, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Contact Number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Re-enter Password'}))
    
    def save(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("Passwords do not match")

        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],  # Use password1
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.save()
        
        vendor = VendorProfile(
            user=user,
            contact_number=self.cleaned_data['contact_number'],
            store_name=self.cleaned_data['store_name'],
        )
        vendor.save()
        

        vendor_group, created = Group.objects.get_or_create(name='Vendor')
        user.groups.add(vendor_group)
        
        return user