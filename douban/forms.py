from django.forms import ModelForm
from douban import models
from django import forms
from django.contrib.auth import get_user_model, authenticate
import re
from django.contrib.auth.forms import ReadOnlyPasswordHashField


def lowercase_email(email):
    """
    Normalize the address by lowercasing the domain part of the email
    address.
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = '@'.join([email_name.lower(), domain_part.lower()])
    return email


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
    username = forms.CharField(min_length=4, max_length=15, required=True,
                               label="User name", help_text='Begin with letter, \
                                               underlined, letters or numbers',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': "Login username",
                                                             'autocomplete': 'off', 'pattern': r'^[a-zA-Z]+[\w_]*'}),
                               error_messages={'required': 'Please input login username',
                                               'invalid': 'username format error',
                                               'max_length': 'Input up to 15 characters',
                                               'min_length': 'Input at least 4 characters'})
    email = forms.EmailField(min_length=5, max_length=30, required=True, label="Email address",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off',
                                                            'placeholder': "Email address",
                                                            'pattern': r'^\w+[\w_]*@\w+\.[a-zA-Z]+'}),
                             error_messages={'required': 'Please input email address', 'invalid': 'Email format error'})
    real_name = forms.CharField(min_length=5, max_length=15, label="Real name", help_text='Begin with letter, \
                                               underlined, letters, space or numbers',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off',
                                                              'placeholder': "User real name",
                                                              'pattern': r'^[a-zA-Z]+[\w_\ ]*'}))
    sex = forms.CharField(label="Sex", widget=forms.Select(choices=models.SEX_CHOICES,
                                                           attrs={'class': 'form-control'}))
    phone_num = forms.CharField(label='Phone number', min_length=5, max_length=15, help_text='Begin with numbers, \
                                               middle line or numbers',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off',
                                                              'placeholder': "User phone number",
                                                              'pattern': r'^\d+[\d\-]*'}))
    password = forms.CharField(min_length=6, max_length=18, label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': "Password"}))
    password2 = forms.CharField(min_length=6, max_length=18, label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': "Confirm password"}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'real_name',
                  'sex', 'phone_num', 'is_active', 'is_admin')

    def clean_username(self):
        user_model = get_user_model()
        username = self.cleaned_data["username"]
        # filter some username register
        n = re.sub('[^\u4e00-\u9fa5a-zA-Z]', '', username)
        filter_name = ['admin', 'root', 'test']
        if n in filter_name:
            raise forms.ValidationError("Can't register %s" % username)

        try:
            user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            return username
        raise forms.ValidationError("%s exist, can't register" % username)

    def clean_email(self):
        user_model = get_user_model()
        email = self.cleaned_data["email"]
        lower_email = lowercase_email(email)
        try:
            user_model.objects.get(email=lower_email)
        except user_model.DoesNotExist:
            return lower_email
        raise forms.ValidationError("%s exist, can't register" % lower_email)

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_real_name(self):
        real_name = self.cleaned_data.get('real_name')
        return real_name

    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')
        return phone_num

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


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username:', required=True)
    password = forms.CharField(
        label='Password:', required=True, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        username = username.strip()
        cleaned_data['username'] = username
        password = cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                return cleaned_data
            else:
                raise forms.ValidationError("Account forbidden login")

        if not username or not password:
            raise forms.ValidationError("Username/password not allowed empty")

        else:
            raise forms.ValidationError("Username and password not matched")
