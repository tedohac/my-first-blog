from django import forms
from .models import Post, Category, Comment

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'text', 'category',)

class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ('title',)

class PostSearchForm(forms.Form):
  title = forms.CharField(required=True)

class CommentForm(forms.ModelForm):
	class Meta:
	    model = Comment
	    fields = ('author', 'text',)