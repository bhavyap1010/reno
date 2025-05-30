from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from .forms import BusinessForm, ServiceRequestForm, ReviewForm, PostSignupForm
from .models import Profile, BusinessProfile, ServiceRequest, Chatroom, Message, ServiceRequestImage
from django.contrib.auth.decorators import login_required
import json
import secrets
from django.http import JsonResponse as jsonresponse, HttpResponseBadRequest as httpresponsebadrequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


from django.shortcuts import render, redirect
from .models import BusinessProfile, ServiceRequest

def home(request):
    if not request.user.is_authenticated:
        return redirect("account_login")  # Redirect to login if not authenticated

    query = request.GET.get('q')
    services = request.GET.getlist('services')  # Get multiple selected services

    businesses = BusinessProfile.objects.all()
    service_requests = ServiceRequest.objects.all()

    # Filter by search query
    if query:
        service_requests = service_requests.filter(title__icontains=query)

    # Filter by multiple services (AND logic)
    if services:
        for service in services:
            service_requests = service_requests.filter(services_needed__icontains=service)

    context = {
        'businesses': businesses,
        'service_requests': service_requests
    }

    return render(request, 'client/home.html', context)

@login_required
def create_or_edit_business_profile(request):
    profile, created = BusinessProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=profile)  # <-- Add request.FILES
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BusinessForm(instance=profile)

    return render(request, 'client/business_form.html', {'form': form})

@login_required
def create_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()

            # Save multiple images
            files = request.FILES.getlist('images')
            for f in files:
                ServiceRequestImage.objects.create(service_request=service_request, image=f)

            return redirect('home')
    else:
        form = ServiceRequestForm()
    return render(request, 'client/service_request_form.html', {'form': form})

@login_required
def delete_service_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    if service_request.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this request.")

    if request.method == 'POST':
        service_request.delete()
        messages.success(request, "Service request deleted successfully.")
        return redirect('home')
    else:
        return HttpResponseForbidden("Invalid request method.")

@login_required
def write_review(request, business_id):
    business = get_object_or_404(BusinessProfile, id=business_id)

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
    business = get_object_or_404(BusinessProfile, id=business_id)
    reviews = business.reviews.all()  # reverse relationship via related_name='reviews'
    return render(request, 'client/business_detail.html', {
        'business': business,
        'reviews': reviews
    })

@login_required
def chatPage(request, room_name=None):
    if request.method == 'POST':
        data = json.loads(request.body)

        other_username = data.get('other_user')
        other_user = get_object_or_404(User, username=other_username)
        current_user = request.user

        # Prevent chatting with self
        if other_user == current_user:
            return httpresponsebadrequest("Cannot start a chat with yourself.")

        # check if a room already exists
        existing_room = Chatroom.objects.filter(participants=current_user).filter(participants=other_user).first()
        if existing_room:
            room = existing_room
        else:
            room = Chatroom.objects.create(room_name=secrets.token_hex(8))
            room.participants.add(current_user, other_user)

        return jsonresponse({'room_name': room.room_name})
    else:
        if not room_name:
            return httpresponsebadrequest("missing room name")

        room = get_object_or_404(Chatroom, room_name=room_name)

        if not room.participants.filter(id=request.user.id).exists():
            return HttpResponseForbidden("you are not authorized to access this chat.")

        # get the other participant
        participants = room.participants.exclude(id=request.user.id)
        other_user = participants.first() if participants.exists() else None

        messages = room.messages.select_related('sender').order_by('timestamp')

        context = {
            'room_name': room.room_name,
            'username': request.user.username,
            'other_user': other_user.username if other_user else 'unknown',
            'messages': messages
        }

        return render(request, 'client/chatpage.html', context)

def user_messages(request):
    Chatrooms = request.user.Chatrooms.all()

    rooms_with_users = []
    for room in Chatrooms:
        other_user = room.participants.exclude(id=request.user.id).first()
        if other_user and room.room_name:  # Avoid empty names or missing users
            rooms_with_users.append((room, other_user))

    return render(request, "client/message.html", {"rooms_with_users": rooms_with_users})

@login_required
def chat_home(request, room_name=None):
    Chatrooms = request.user.Chatrooms.all()

    # build the sidebar list
    rooms_with_users = []
    for room in Chatrooms:
        other_user = room.participants.exclude(id=request.user.id).first()
        if other_user and room.room_name:
            rooms_with_users.append((room, other_user))

    # load the current room and messages (if selected)
    messages = []
    other_user = None
    selected_room = None

    if room_name:
        selected_room = get_object_or_404(Chatrooms, room_name=room_name)

        if not selected_room.participants.filter(id=request.user.id).exists():
            return HttpResponseForbidden("you are not authorized to access this chat.")

        messages = selected_room.messages.select_related('sender').order_by('timestamp')
        other_user = selected_room.participants.exclude(id=request.user.id).first()

    context = {
        'rooms_with_users': rooms_with_users,
        'room_name': selected_room.room_name if selected_room else '',
        'messages': messages,
        'username': request.user.username,
        'other_user': other_user.username if other_user else '',
    }

    return render(request, 'client/chat_home.html', context)



@csrf_exempt  # Allow POST requests without CSRF token for debugging
@login_required
def start_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            other_username = data.get('other_user')
            other_user = get_object_or_404(User, username=other_username)
            current_user = request.user

            # Prevent chatting with self
            if other_user == current_user:
                return jsonresponse({'error': "Cannot start a chat with yourself."}, status=400)

            # Check if a room already exists
            existing_room = Chatroom.objects.filter(participants=current_user).filter(participants=other_user).first()
            if existing_room:
                room = existing_room
            else:
                room = Chatroom.objects.create(room_name=secrets.token_hex(8))
                room.participants.add(current_user, other_user)

            return jsonresponse({'room_name': room.room_name})
        except Exception as e:
            return jsonresponse({'error': str(e)}, status=500)
    else:
        return jsonresponse({'error': "Invalid request method."}, status=405)

@login_required
def choose_account_type_and_username(request):
    # If profile already exists, skip this step
    if hasattr(request.user, 'profile'):
        return redirect('/')

    if request.method == 'POST':
        form = PostSignupForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            account_type = form.cleaned_data['account_type']

            existing_user = User.objects.exclude(pk=request.user.pk).filter(username=new_username).first()

            if existing_user:
                if existing_user.email == request.user.email:
                    existing_user.delete()
                else:
                    messages.error(request, "That username is already taken.")
                    return render(request, 'client/choose_account_type_and_username.html', {'form': form})

            request.user.username = new_username
            request.user.save()
            Profile.objects.create(user=request.user, account_type=account_type)
            return redirect('/')
    else:
        initial = {}
        if not hasattr(request.user, 'profile'):
            initial['username'] = request.user.username
        form = PostSignupForm(initial=initial)

    return render(request, 'client/choose_account_type_and_username.html', {'form': form})

def service_request_detail(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    images = service_request.images.all()
    print(images)
    return render(request, 'client/service_request_detail.html', {
        'service_request': service_request,
        'images': images
    })
