from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import SignUpForm, VerificationCodeForm, CustomAuthenticationForm, BusinessProfileForm, servicerequestform, ReviewForm
from .emailVerification import AccountActivationManager
from .models import businessProfile, serviceRequest, chatroom, Messages
from django.contrib.auth.decorators import login_required


def home(request):
    if not request.user.is_authenticated:
        return redirect("register")

    query = request.GET.get('q')  # Get the search term from the query string

    businesses = businessProfile.objects.all()

    if query:
        service_requests = serviceRequest.objects.filter(title__icontains=query)
    else:
        service_requests = serviceRequest.objects.all()

    context = {
        'businesses': businesses,
        'service_requests': service_requests
    }

    return render(request, 'client/home.html', context)

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

@login_required
def create_or_edit_business_profile(request):
    profile, created = businessProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BusinessProfileForm(instance=profile)

    return render(request, 'client/business_form.html', {'form': form})

@login_required
def create_service_request(request):
    if request.method == 'POST':
        form = servicerequestform(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            return redirect('home')
    else:
        form = servicerequestform()
    return render(request, 'client/service_request_form.html', {'form': form})

@login_required
def write_review(request, business_id):
    business = get_object_or_404(businessProfile, id=business_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.business = business
            review.user = request.user
            review.save()
            return redirect('home')  # Or redirect to business detail
    else:
        form = ReviewForm()

    return render(request, 'client/write_review.html', {'form': form, 'business': business})

def business_detail(request, business_id):
    business = get_object_or_404(businessProfile, id=business_id)
    reviews = business.reviews.all()  # reverse relationship via related_name='reviews'
    return render(request, 'client/business_detail.html', {
        'business': business,
        'reviews': reviews
    })
    
@login_required
def chatPage(request, room_name):

    users = room_name.split('_')
    other_user = users[1] if users[0] == request.user.username else users[0]

    room, _ = chatroom.objects.get_or_create(room_name=room_name)
    messages = room.messages.select_related('sender').order_by('timestamp')


    context = {
        'room_name': room_name,
        'username': request.user.username,
        'other_user': other_user,
        'messages': messages
    }
    
    other_user = get_object_or_404(User, username=other_user)

    room, _ = chatroom.objects.get_or_create(room_name=room_name)
    room.participants.add(request.user)
    room.participants.add(other_user)
    
    return render(request, 'client/chatPage.html', context)

def user_messages(request):
    
    chatrooms = request.user.chatrooms.all()
    return render(request, "client/message.html", {"chatrooms": chatrooms})
