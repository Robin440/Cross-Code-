from django.contrib import admin

# Register your models here.
from account.models import CustomUser, Verification

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'verified', 'created_at', 'updated_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)
    filter_horizontal = ()
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('UUID', {'fields': ('uuid',)}),
    )
    readonly_fields = ('id', 'created_at', 'updated_at')


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('username', 'email')
        return self.readonly_fields 
    
@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'purpose', 'is_used', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'token', 'otp', 'purpose')
    ordering = ('-created_at',)
    list_filter = ('purpose', 'is_used')
    fieldsets = (
        (None, {'fields': ('user', 'token', 'otp', 'purpose')}),
        ('Status', {'fields': ('is_used',)}),
        ('Timestamps', {'fields': ('created_at', 'expires_at')}),
        ('UUID', {'fields': ('uuid',)}),
    )
    readonly_fields = ('uuid', 'created_at')    


