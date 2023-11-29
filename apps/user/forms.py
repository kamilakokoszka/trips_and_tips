from django import forms

from apps.core.models import Profile


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    set_default_profile_picture = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Profile
        fields = ['bio', 'website', 'picture', 'set_default_profile_picture']
