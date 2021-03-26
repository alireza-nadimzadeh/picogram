from django import forms
from django.contrib.auth.models import User
from .models import Comment


class NewCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"rows": 5, "cols": 20}), max_length=1024, label='',)

    class Meta:
        model = Comment
        fields = ['content']
