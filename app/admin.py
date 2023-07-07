from django.contrib import admin
from app.models import Employee, Task, User
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



class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['user_name']
    list_filter = ('job_title', 'city')
    list_display = ('emp_number', 'surname', 'user_name', 'job_title')


admin.site.register(User, UserModelAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Task)
