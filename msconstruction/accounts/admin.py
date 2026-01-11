from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile


# ---------------------------
# INLINE PROFILE (SHOW INSIDE USER)
# ---------------------------
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    readonly_fields = ('profile_photo_preview',)

    def profile_photo_preview(self, obj):
        if obj.profile_photo:
            return (
                f'<img src="{obj.profile_photo.url}" '
                f'style="width:100px;height:100px;border-radius:50%;" />'
            )
        return "No Image"

    profile_photo_preview.allow_tags = True
    profile_photo_preview.short_description = "Profile Photo"


# ---------------------------
# EXTENDED USER ADMIN
# ---------------------------
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
    )
    search_fields = ('username', 'email')


# ---------------------------
# REGISTER
# ---------------------------
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
