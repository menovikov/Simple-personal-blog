from django import forms
from pagedown.widgets import PagedownWidget

from .models import Post, Tag, Subscriber

class PostForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget(show_preview=False))
	class Meta:
		model = Post
		fields = ['title', 'draft', 'image', 'content', 'tag']

class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ['title',]

class SubscriberForm(forms.ModelForm):
	class Meta:
		model = Subscriber
		fields = ['name', 'email_address',]