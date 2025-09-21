from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    # Only the single optional cover image is in the form
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']  # 'image' is optional
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter your post title...',
                'style': 'width:100%; padding:12px; border:1px solid #3b2f2f; border-radius:6px; font-family:Georgia, serif; margin-bottom:15px; background-color:#fdfaf3;'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': "What's on your mind?",
                'rows': 6,
                'style': 'width:100%; padding:12px; border:1px solid #3b2f2f; border-radius:6px; font-family:Roboto, sans-serif; resize:vertical; margin-bottom:15px; background-color:#fdfaf3;'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
