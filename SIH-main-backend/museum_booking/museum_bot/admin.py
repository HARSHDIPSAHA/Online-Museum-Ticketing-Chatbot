from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Trip, Museum

# Define the CustomUser admin class
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Define the fields to display in the list view
    list_display = ('username', 'phone_number', 'email', 'verified', 'is_staff', 'is_superuser')
    # Define fields to search on
    search_fields = ('username', 'phone_number', 'email')
    # Define ordering of records
    ordering = ('username',)
    # Define fields to be displayed on the user detail view
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'otp', 'verified')}),
    )
    # Define fields to be included in the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'otp', 'verified')}),
    )

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)

# Register the Trip model
class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'museum_name', 'transaction_id', 'confirmed')
    search_fields = ('museum_name', 'user__phone_number')
    list_filter = ('confirmed',)
    ordering = ('-confirmed', 'museum_name')

admin.site.register(Trip, TripAdmin)

class MuseumAdmin(admin.ModelAdmin):
    list_display = ('MUSEUM_NAME', 'PINCODE', 'ADULTPRICE', 'CHILDPRICE')
    search_fields = ('MUSEUM_NAME', 'PINCODE')
    list_filter = ('ADULTPRICE', 'CHILDPRICE')
    ordering = ('MUSEUM_NAME',)

# Register the Museum model with the MuseumAdmin class
admin.site.register(Museum, MuseumAdmin)