from django import forms
from .models import Comment, Post, PostFiles, TextVideoClips

class AddPostForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': "What's about this post?"}))
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control", 'placeholder': 'Enter text of your post'}))
    tags = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    class Meta:
        model = Post
        fields = ['body', 'title', 'status', 'tags',]


class Files_for_post(forms.ModelForm):
    class Meta:
        model = PostFiles
        fields = ['image', 'audio', 'video']


class TextClipsForm(forms.ModelForm):
    class Meta:
        model = TextVideoClips
        fields = ['text', 'name_of_file']


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'E-Mail'}))
    to = forms.EmailField(required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'To'}))
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={"class": "form-control mb-1", 'placeholder': 'Comments'}))

class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control", 'placeholder': 'Enter your comment'}))

    class Meta:
        model = Comment
        fields = ['body']


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Enter search term...'}))