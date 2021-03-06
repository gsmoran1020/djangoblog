from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Override of save method allows us to implement image resizing for user submitted profile images
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path).convert('RGB')

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)