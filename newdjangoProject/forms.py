from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, RadioSelect, SelectDateWidget

from newdjangoProject.models import Order, Student


class InterestForm(forms.Form):
    choice = [('1', 'Yes'), ('0', 'No')]
    interested = forms.CharField(label='Interested', widget=forms.RadioSelect(choices=choice))
    levels = forms.IntegerField(min_value=1, max_value=10)
    comments = forms.CharField(label='Additional Comments', widget=forms.Textarea(), required=False)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('student', 'course', 'levels', 'order_date')
        widgets = {
            'student': RadioSelect(),
            'order_date': SelectDateWidget()
        }


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('avatar',)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ResetPasswordForm(forms.Form):
    username = forms.CharField(label='Username')


class RegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 max_length=32, help_text='First name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                max_length=32, help_text='Last name')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), max_length=64,
                             help_text='Enter a valid email address')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user
