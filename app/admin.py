from django.contrib import admin
from app.models import User,Blog
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email','first_name', 'last_name', 'is_verified',)
    list_filter = ('is_superuser',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_verified', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('id', 'email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("published_at", "updated_at", "created_at", "is_published", "publish_choices", "blog_content", "blog_image", "blog_title", "user")
