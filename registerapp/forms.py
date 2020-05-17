from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customuser, Bio
from crispy_forms.helper import FormHelper
from django.contrib.auth import authenticate, login, logout


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = Customuser
        fields = ['email', 'password1', 'password2']

class LoginForm(forms.Form):

    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email address', 'class':'form-control',  'id':'inputEmail'}), label="Email address")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control', 'id':'inputPassword'}))

    """def clean(self):
        cleaned_data = super().clean()

        email_data = self.cleaned_data.get('email')
        password_data = self.cleaned_data.get('password')
        custom_user = authenticate(username = email_data , password=password_data)
        if custom_user is None:
            print('incorrect password')
            raise forms.ValidationError(" Password and Email do not match ")
        else:
            print(" not None ")

        return cleaned_data """

    """def clean_password(self):

        email_data = self.cleaned_data.get('email')
        password_data = self.cleaned_data.get('password')
        custom_user = authenticate(username = email_data , password=password_data)
        if custom_user is None:
            print('incorrect password')
            raise forms.ValidationError(" Password and Email do not match ")
        else:
            print(" not None ")

        return password_data """

"""
class LoginForm(forms.Form):
    [...]
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email address'}), label="Email address")
        password = forms.CharField(widget=forms.PasswordInput)

        self.helper = FormHelper()
        self.helper.form_class = "form-label-group"
        self.helper.form_method = 'post'
"""


class Overall_Form(forms.ModelForm):
    class Meta:
        model = Bio
        fields = ['first_name','last_name','middle_name','gender','date_of_birth',
                'hobbies','nok1_name','nok1_phone','nok1_relationship',
                'nok2_name','nok2_phone','nok2_relationship','primary','secondary','tertiary',
                  'passport','o_level','birth_cert','indegeneship_cert','degree_cert',
                  'ref1_name','ref1_phone','ref1_occupation','ref2_name','ref2_phone',
                  'ref2_occupation']

        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'middle_name': 'Middle Name',
                  'gender': 'Gender', 'date_of_birth': 'Date of Birth', 'hobbies': 'Hobbies',
                  'nok1_name': 'Next of Kin\'s Name  ', 'nok1_phone': 'Next of kin\'s Phone',
                  'nok1_relationship': 'Relationship', 'nok2_name': '2nd Next of Kin\'s Name  ', 'nok2_phone': 'Next of kin\'s Phone',
                  'nok2_relationship': 'Relationship'}

class Disabled_Form(forms.ModelForm):
    class Meta:
        model = Bio
        fields = ['first_name','last_name','middle_name','gender','date_of_birth',
                'hobbies','nok1_name','nok1_phone','nok1_relationship',
                'nok2_name','nok2_phone','nok2_relationship','primary','secondary','tertiary',
                  'passport','o_level','birth_cert','indegeneship_cert','degree_cert',
                  'ref1_name','ref1_phone','ref1_occupation','ref2_name','ref2_phone',
                  'ref2_occupation']

        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'middle_name': 'Middle Name',
                  'gender': 'Gender', 'date_of_birth': 'Date of Birth', 'hobbies': 'Hobbies',
                  'nok1_name': 'Next of Kin\'s Name  ', 'nok1_phone': 'Next of kin\'s Phone',
                  'nok1_relationship': 'Relationship', 'nok2_name': '2nd Next of Kin\'s Name  ', 'nok2_phone': 'Next of kin\'s Phone',
                  'nok2_relationship': 'Relationship'}
    def __init__(self, *args, **kwargs):
        super(Disabled_Form, self).__init__(*args, **kwargs)
        self.fields['first_name'].disabled = True
        self.fields['last_name'].disabled = True
        self.fields['middle_name'].disabled = True
        self.fields['gender'].disabled = True

