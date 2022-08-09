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


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ("username", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user



