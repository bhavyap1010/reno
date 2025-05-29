from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, BusinessProfile, ServiceRequest, Review, Chatroom, Message
from .forms import SignUpForm

# Inline Profile inside User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extend the User Admin
class UserAdmin(BaseUserAdmin):
    add_form = SignUpForm
    inlines = (ProfileInline,)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

# BusinessProfile Admin
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user', 'service_location', 'display_services')

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'

    def display_services(self, obj):
        return ", ".join(obj.services)
    display_services.short_description = 'Services'

# ServiceRequest Admin
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'location')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height:80px; max-width:120px; border-radius:8px;" />'
        return "-"
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class chatRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name',)
    filter_horizontal = ('participants',)

# Re-register User and register all models
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(BusinessProfile, BusinessProfileAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)
admin.site.register(Review)
admin.site.register(Chatroom, chatRoomAdmin)
admin.site.register(Message)
