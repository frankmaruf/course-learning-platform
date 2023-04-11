from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Role, CustomUser,Course,SidebarItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
#     last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
#     email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
#     role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'role', 'password1', 'password2', )


class SidebarItemForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=SidebarItem.objects.all(), required=False)
    
    class Meta:
        model = SidebarItem
        fields = ['title', 'url', 'parent','position']
        widgets = {
            'position': forms.HiddenInput(),
        }




class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    password1 = forms.CharField(max_length=30, required=False)
    password2 = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    
    # role = forms.ModelChoiceField(queryset=Role.objects.all())

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email','password1', 'password2',)
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
    
# class CustomUserCreationForm(UserCreationForm):
#     role = forms.ModelChoiceField(queryset=Role.objects.all())

#     class Meta:
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields + ('role',)

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = self.cleaned_data['role']
#         if commit:
#             user.save()
#         return user

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'image']

    image = forms.ImageField(required=False)