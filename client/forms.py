from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, BusinessProfile, ServiceRequest, Review
from allauth.account.forms import SignupForm, LoginForm

class CustomSignupForm(SignupForm):
    account_type = forms.ChoiceField(
        choices=[('individual', 'Individual'), ('business', 'Business')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def save(self, request):
        user = super().save(request)
        Profile.objects.create(
            user=user,
            account_type=self.cleaned_data['account_type']
        )
        return user

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget = forms.TextInput(
            attrs={"placeholder": "Username or Email", "class": "form-control"}
        )
        self.fields["password"].widget.attrs.update({"class": "form-control"})

    def clean(self):
        # IMPORTANT: Call parent clean first to initialize internal allauth state
        cleaned_data = super().clean()

        login = self.cleaned_data.get("login")
        password = self.cleaned_data.get("password")

        # Authenticate by username or email
        user = authenticate(self.request, username=login, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=login)
                user = authenticate(self.request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is None:
            raise forms.ValidationError("Invalid login credentials.")

        self.user = user
        self.user_cache = user
        return cleaned_data

class PostSignupForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    account_type = forms.ChoiceField(
        choices=[('individual', 'Individual'), ('business', 'Business')],
        required=True
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

class BusinessForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ['name', 'services', 'service_location', 'image', 'status']
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


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return [single_file_clean(data, initial)]


class ServiceRequestForm(forms.ModelForm):
    images = MultipleFileField(required=False)  # <-- Not "image", use many

    class Meta:
        model = ServiceRequest
        fields = ['title', 'services_needed', 'location', 'description']

        widgets = {
            'services_needed': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
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
