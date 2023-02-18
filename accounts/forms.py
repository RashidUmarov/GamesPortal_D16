from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

"""
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")


class Meta:
    model = User
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "password1",
        "password2",
    )
"""

class MyUserProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]
        labels = {'username': ('Логин'),
                  'first_name': ('Имя'),
                  'last_name': ('Фамилия'),
                  }
        help_texts = {'username': ('Желаемый никнейм'),
                      'first_name': ('Укажите ваше имя'),
                      'last_name': ('Ваша фамилия'),
                      }
