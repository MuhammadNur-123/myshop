from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField, PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer ,Contact ,Review ,NewsletterSubscription ,Blog, OrderPlaced

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'})),
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'})),
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'})),
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
 old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True,  'class':'form-control'}))
 new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
 new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))
 
class MyPasswordResetForm(PasswordResetForm):
 email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
 new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
 new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ['name','locality','city','division','zipcode']
    widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}), 'city':forms.TextInput(attrs={'class':'form-control'}), 
    'division':forms.Select(attrs={'class':'form-control'}),
    'zipcode':forms.NumberInput(attrs={'class':'form-control'})}       


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'YOUR NAME'}),
            'email': forms.EmailInput(attrs={'placeholder': 'YOUR EMAIL'}),
            'subject': forms.TextInput(attrs={'placeholder': 'SUBJECT'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'MESSAGE'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }
class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription  # Link the form to the model
        fields = ['email']  # Specify which fields from the model you want to use


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'tags', 'image']

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class OrderPlacedForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = ['customer', 'product', 'quantity', 'status']
        labels = {
            'customer': 'Select Customer',
            'product': 'Select Product',
            'quantity': 'Quantity',
            'status': 'Order Status',
        }
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
