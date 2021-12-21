from django import forms
from django.db.models.fields import TextField
from django.forms.widgets import Textarea
from .models import Profile,Project,Rating

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_pic','contact']
        widgets = {
            'bio': Textarea(attrs={'cols': 30, 'rows': 3}),
        }
class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image','description','link']
        widgets = {
            'description': Textarea(attrs={'cols' : 20, 'rows' : 5}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        fields=['design_rate','usability_rate','content_rate']