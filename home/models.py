from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    Model representing a blog/chat post with optional cover image and likes.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(
        upload_to='posts/', 
        blank=True, 
        null=True,
        help_text="Optional cover image for the post"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    likes = models.ManyToManyField(
        User, 
        related_name='liked_posts', 
        blank=True,
        help_text="Users who liked this post"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        """
        Returns the total number of likes for the post.
        """
        return self.likes.count()

    def __str__(self):
        return self.title


class PostImage(models.Model):
    """
    Model to store multiple images for a single post (gallery images).
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='posts/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)  # <-- add this

    def __str__(self):
        return f"Image for {self.post.title}"



class Comment(models.Model):
    """
    Model representing a comment on a post.
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
