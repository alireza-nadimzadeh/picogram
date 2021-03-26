from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(default='def.jpg')
    likes = models.ManyToManyField(
        User, related_name='post_likes', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    content = models.TextField(max_length=512)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE, null=True)
    created_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})
