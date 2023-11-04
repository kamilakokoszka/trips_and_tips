from django import forms

from apps.core.models import Profile


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)
    website = forms.CharField(max_length=255)
    picture = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['bio', 'website', 'picture']
