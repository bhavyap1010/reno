from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, BusinessProfile, ServiceRequest, Review

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password Confirmation'
        })
    )
    account_type = forms.ChoiceField(
        choices=[('', 'Select Account Type'), ('individual', 'Individual'), ('business', 'Business Owner')],
        required=True,
        widget=forms.Select(attrs={
            'class': 'select_option',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'account_type')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
            })
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            profile = Profile.objects.create(user=user, account_type=self.cleaned_data['account_type'])
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
        })
    )

class VerificationCodeForm(forms.Form):
    code = forms.CharField(label='Code', max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Enter verification code'}))

class BusinessForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ['name', 'services', 'service_location', 'image']  # <-- Add 'image'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}),
            'services': forms.CheckboxSelectMultiple(),
            'service_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),  # <-- Add widget for image
        }

    def clean_services(self):
        services = self.cleaned_data.get('services')
        if not services:
            raise forms.ValidationError("Please select at least one service.")
        return services

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'services_needed', 'location', 'description', 'image']  # <-- Add 'image'
        widgets = {
            'services_needed': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Title'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your request'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),  # <-- Add widget for image
        }

    def clean_services_needed(self):
        services = self.cleaned_data.get('services_needed')
        if not services:
            raise forms.ValidationError("Please select at least one service.")
        return services

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
