from django import forms
from .models import Question, Choice, Comment

class CommentForm(forms.Form):
	class Meta:
		model = Comment
	
	def __init__(self, *args, **kwargs):
		self.fields["question"] = forms.CharField(widget=forms.HiddenInput())
		super(CommentForm, self).__init__(self, *args, **kwargs)