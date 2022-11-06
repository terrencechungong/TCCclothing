from cProfile import Profile
from .models import Projects, Review
from  django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, CreateView
from django.views import generic

class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'demo_link', 'source_link', 'tags', 'featured_image']
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone_number','password1','password2','gender']

class CustomUserUpdateForm(UpdateView):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone_number']

# create update form for users
class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone_number']

class CommentForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body']
