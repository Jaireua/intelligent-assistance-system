# Import the necessary modules
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserImage(models.Model):
    # Relationship field
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Image field
    face_image = models.ImageField(upload_to='user_faces/')

    # Str representation of the model
    def __str__(self):
        return self.user.username
