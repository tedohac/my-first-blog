from django import forms
from .models import Post

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'text',)

class PostSearch(forms.Form):
  title = forms.CharField(required=True)