# Import libraries
from django.db import models # Define database model
from django.contrib.auth.models import User # Model user defined by django

# Create model Users
class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    identification = models.ForeignKey(User, on_delete=models.CASCADE, related_name='identification')
    face_image = models.ImageField(upload_to='face_images/')

    def __str__(self):
        return self.user.username