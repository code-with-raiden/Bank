from django import  forms
from .models import  Account

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name','phone','dob','email','aadhar','pan','photo','gender','address','state','nominee','nominee_phone','nominee_relation']