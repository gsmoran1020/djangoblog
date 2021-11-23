from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # CASCADE ensures that all posts are deleted if the User is
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def __str__(self):
        return self.title

    # doing this in the model allows the CreateView to know where to send the user once it is done creating the post.
    # In this case it sends it to the page for the newly created post.
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.post.title} - comment'