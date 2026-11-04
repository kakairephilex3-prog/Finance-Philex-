from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FinancialRecord

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class FinancialRecordForm(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ("record_type", "amount", "description", "reference", "record_date")
        widgets = {"record_date": forms.DateInput(attrs={"type": "date"})}
