from django.contrib import admin
from .models import (
    User,
    RoleType,
    Permissions,
    UserRole,
    PersonalDetails,
    AuditLog
)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'mobile_number', 'is_org_admin', 'is_verified', 'is_active', 'is_admin', 'role')
#     search_fields = ('email', 'name', 'mobile_number')
#     list_filter = ('is_org_admin', 'is_verified', 'is_active', 'is_admin', 'role')
#     ordering = ('created_at',)
#     readonly_fields = ('created_at', 'updated_at')

#     def get_role(self, obj):
#         return obj.role.role_name if obj.role else None


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'email', 
        'mobile_number', 
        'get_role',  # Improved readability
        'client', 
        'is_org_admin', 
        'is_verified', 
        'is_active', 
        'is_admin',
    )
    search_fields = ('email', 'name', 'mobile_number', 'client__client_name',)  # Add search functionality for client name
    list_filter = (
        'is_org_admin', 
        'is_verified', 
        'is_active', 
        'is_admin', 
        'role', 
        'client__region',  # Added filtering by client region
    )
    ordering = ('-created_at',)  # Order by creation date (most recent first)
    readonly_fields = ('created_at', 'updated_at',)

    def get_role(self, obj):
        """Get the role name for the user."""
        return obj.role.role_name if obj.role else "No Role Assigned"

    get_role.short_description = 'Role'  # Set the column name in the admin panel

    def get_queryset(self, request):
        """Override queryset to include related fields for performance."""
        queryset = super().get_queryset(request)
        return queryset.select_related('role', 'client')

    fieldsets = (
        ("Personal Information", {
            'fields': ('name', 'email', 'mobile_number', 'otp')
        }),
        ("Role & Client Details", {
            'fields': ('role', 'client')
        }),
        ("Status", {
            'fields': ('is_verified', 'is_active', 'is_admin', 'is_org_admin', 'is_staff')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )

# Custom admin for RoleType model
@admin.register(RoleType)
class RoleTypeAdmin(admin.ModelAdmin):
    list_display = ('role_name', )
    search_fields = ('role_name', )
    #filter_horizontal = ('role_permissions',)

# Custom admin for Permissions model
@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('route_path',)
    search_fields = ('route_path',)


# Custom admin for UserRole model
@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__name', 'role__role_name')
    list_filter = ('role',)


# Custom admin for PersonalDetails model
@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'gender', 'phone_no', 'designation')
    search_fields = ('user__name', 'first_name', 'last_name', 'phone_no')
    list_filter = ('gender',)


# Custom admin for AuditLog model
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'method', 'path', 'status_code', 'duration', 'timestamp')
    search_fields = ('user__name', 'path', 'method')
    list_filter = ('status_code', 'method', 'timestamp')
    readonly_fields = ('timestamp',)
