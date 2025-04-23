from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, businessProfile, serviceRequest


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

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = businessProfile
        fields = ['name', 'services', 'service_location']

class servicerequestform(forms.ModelForm):
    class Meta:
        model = serviceRequest
        fields = ['title', 'services_needed', 'location', 'description']

