# Import the necessary Django admin module
from django.contrib import admin
from .models import UserImage

# Register models with the Django admin interface
@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserImage model.
    
    This class customizes how the UserImage model appears and functions
    in the Django admin interface.
    """
    list_display = ('user', 'face_image')  # Fields to display in the list view
    search_fields = ('user__username',)    # Fields for search functionality
    list_filter = ('user',)                # Fields for filtering