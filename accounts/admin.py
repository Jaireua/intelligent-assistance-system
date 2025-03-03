# Import the necessary Django admin module
from django.contrib import admin
from .models import UserImages  

# Register models with the Django admin interface
@admin.register(UserImages)
class UserImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserImages model.
    
    This class customizes how the UserImages model appears and functions
    in the Django admin interface.
    """
    list_display = ('user', 'face_image')  # Fields to display in the list view
    search_fields = ('user__username',)    # Fields for search functionality
    list_filter = ('user',)                # Fields for filtering