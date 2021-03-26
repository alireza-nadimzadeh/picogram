from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    f_name = models.CharField(max_length=64, blank=True, null=True)
    l_name = models.CharField(max_length=64, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='def.jpg', blank=True, null=True)
    followers = models.ManyToManyField(
        User, related_name='followers', blank=True, null=True,)
    following = models.ManyToManyField(
        User, related_name='following', blank=True, null=True,)

    def get_number_of_followers(self):
        return self.followers.count()

    def get_number_of_following(self):
        return self.following.count()

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return "/profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
