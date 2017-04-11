from django.forms import ModelForm
from douban import models
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class DoubanForm(ModelForm):
    class Meta:
        model = models.Douban
        fields = '__all__'


class UserProfileForm(ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = []


class UserProfileCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('username', 'email', 'real_name',
                  'sex', 'phone_num', 'is_active', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserProfileCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserProfileChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    username = forms.CharField(min_length=5, max_length=15, required=True,
                               disabled=True, label="User name",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(min_length=5, max_length=30, required=True, label="Email address",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    real_name = forms.CharField(min_length=5, max_length=15, label="Real name",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    sex = forms.CharField(label="Sex", widget=forms.Select(choices=models.SEX_CHOICES,
                                                           attrs={'class': 'form-control'}))
    phone_num = forms.CharField(label='Phone number', min_length=5, max_length=15,
                                widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        fields = ('username', 'email', 'real_name',
                  'sex', 'phone_num')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
