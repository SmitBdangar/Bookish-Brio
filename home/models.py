from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags

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
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts', help_text="Tags for this post")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        """
        Returns the total number of likes for the post.
        """
        return self.likes.count()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.content:
            import bleach
            allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'blockquote', 'code', 'pre', 'img']
            allowed_attrs = {
                'a': ['href', 'title', 'target'],
                'img': ['src', 'alt', 'title']
            }
            self.content = bleach.clean(self.content, tags=allowed_tags, attributes=allowed_attrs, strip=True)
        super().save(*args, **kwargs)

    @property
    def preview_content(self):
        return strip_tags(self.content)

    def reading_time(self):
        import math
        words = len(strip_tags(self.content).split())
        minutes = math.ceil(words / 200)
        return f"{minutes} min read"


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
    created_at = models.DateTimeField(auto_now_add=True)

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


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Follow(models.Model):
    """
    Model representing a user following another user.
    """
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class Profile(models.Model):
    """
    User profile model extending the built-in User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Social Media Links
    instagram_link = models.URLField(max_length=200, blank=True)
    twitter_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
