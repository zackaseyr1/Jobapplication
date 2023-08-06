from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)




class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description']




class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'submission_time', 'duration','capacity', 'location', 'position_level', 'education_level', 'experience']




class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['full_name', 'location', 'email', 'phone_number', 'education', 'skills', 'age', 'gender','resume']