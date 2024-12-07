from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Оставьте ваш комментарий...', 'rows': 5, 'cols': 5}),
        }