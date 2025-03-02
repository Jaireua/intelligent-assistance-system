# Import the necessary modules for database models
from django.db import models
from django.contrib.auth.models import User

# Define the data models for the application
class UserImage(models.Model):
    """
    Model for storing facial images of users.
    
    This model is used by the facial authentication system to store and retrieve
    facial images that are captured during user registration. Each image is linked
    to a specific user account and is used for facial recognition during login.
    """
    # Foreign key relationship with Django's User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                            verbose_name="Usuario",
                            help_text="Usuario al que pertenece esta imagen facial")
    
    # Field for storing the facial image file
    face_image = models.ImageField(upload_to='user_faces/', 
                                  verbose_name="Imagen facial",
                                  help_text="Imagen facial capturada durante el registro")

    def __str__(self):
        """Returns the username as the string representation of this object."""
        return self.user.username
    
    # Model metadata
    class Meta:
        verbose_name = "Imagen de Usuario"
        verbose_name_plural = "Imágenes de Usuarios"
