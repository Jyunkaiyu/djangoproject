from cProfile import label
from dataclasses import field
from django.forms import ModelForm
from .models import Test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
         label=_('電子信箱'),
         widget=forms.EmailInput(attrs={'autocomplete': 'email','class': 'user_input_bg'}),
         error_messages={
             'invalid': '請輸入有效電子信箱',
             'required': '尚未輸入電子信箱',
         }
     )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class': 'user_input_bg'}),
        help_text=password_validation.password_validators_help_text_html(),
        error_messages={'required': '尚未輸入密碼'},
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class': 'user_input_bg'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        error_messages={'required': '尚未輸入確認密碼'},
    )
    error_messages = {
         'password_mismatch': _('兩次密碼輸入不同'),
     }
    username=forms.CharField(
        label=_('使用者帳號'),
        widget=forms.TextInput(attrs={'class': 'user_input_bg'})
    )
    first_name=forms.CharField(
        label=_('使用者名稱'),
        widget=forms.TextInput(attrs={'class': 'user_input_bg'})
    )
    class Meta:
        model = User
        fields = ("username","email","first_name")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'user_input_bg'}),
            'email': forms.TextInput(attrs={'class': 'user_input_bg'}),
            'first_name':forms.TextInput(attrs={'class': 'user_input_bg'}),
            
        }
class User_form(ModelForm):
    email = forms.EmailField(
         label=_('電子信箱'),
         widget=forms.EmailInput(attrs={'autocomplete': 'email','class': 'user_input_bg input_font','readonly':'ture'}),
         error_messages={
             'invalid': '請輸入有效電子信箱',
             'required': '尚未輸入電子信箱',
         }
     )
    class Meta:
        model=User
        fields=("email","first_name","last_name")
        widgets = {
            'email': forms.TextInput(attrs={'class': 'user_input_bg input_font','readonly':'ture'}),
            'first_name': forms.TextInput(attrs={'class': 'user_input_bg input_font','readonly':'ture'}),
            'last_name': forms.TextInput(attrs={'class': 'user_input_bg input_font','readonly':'ture'}),
        }
# ,'readonly':'ture'