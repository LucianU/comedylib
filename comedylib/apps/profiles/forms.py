from django import forms

from profiles.models import Playlist


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('title',)


class SettingsForm(forms.Form):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'incorrect_oldpass': "The old password that you provided is incorrect.",
    }
    picture = forms.ImageField(required=False)
    oldpassword = forms.CharField(label="Old Password",
        widget=forms.PasswordInput)
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.",
        required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SettingsForm, self).__init__(*args, **kwargs)

    def clean_oldpassword(self):
        oldpassword = self.cleaned_data.get('oldpassword')
        if not self.request.user.check_password(oldpassword):
            raise forms.ValidationError(
                self.error_messages['incorrect_oldpass']
            )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2
