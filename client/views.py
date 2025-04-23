from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import SignUpForm, VerificationCodeForm, CustomAuthenticationForm
from .emailVerification import AccountActivationManager


def home(request):
    
    if not request.user.is_authenticated:
        return redirect("register")

    return render(request, "client/home.html")

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        # Check if the email already exists
        email = form.cleaned_data.get('email') if form.is_valid() else None
        if email and User.objects.filter(email=email).exists():
            form.add_error('email', 'An account with this email already exists.')
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            recipient_email = form.cleaned_data.get('email')
            account_activation_manager = AccountActivationManager()
            subject = "Verification Email From Business Idea"
            verification_code = account_activation_manager.token_generator()
            request.session['verification_code'] = verification_code
            body = verification_code
            
            account_activation_manager.send_email(subject, body, recipient_email)  
            return redirect('/verify')
        
    else:
        form = SignUpForm()
    
    return render(request, 'client/signUp.html', {'form': form})

def verify(request):
    
    verification_code = request.session.get('verification_code')
    
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            
            user_reply = form.cleaned_data.get('code').strip()  # Strip any extra spaces
            verification_code = str(verification_code).strip() if verification_code is not None else None
            
            if str(user_reply) == str(verification_code):
                                
                profile = request.user.profile
                profile.email_is_verified = True
                profile.save()  # Save the updated profile
          
                return redirect('/home')
            else:
                # Verification failed
                form.add_error('code', 'Invalid verification code')
    
    else:
        form = VerificationCodeForm()
    
    return render(request, 'client/verify.html', {'form': form})

def signIn(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after successful login
            else:
                # Add an error message if authentication fails
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'client/login.html', {'form': form})
