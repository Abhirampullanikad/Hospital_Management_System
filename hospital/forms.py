from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Doctor, Patient, Prescription
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import get_user_model
User = get_user_model()



class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=20)
    symptoms = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'patient'
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                mobile=self.cleaned_data['mobile'],
                symptoms=self.cleaned_data['symptoms']
            )
        return user

class PatientUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_pic', 'password1', 'password2']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address', 'mobile', 'status', 'symptoms', 'profile_pic', 'assignedDoctor']
        widgets = {
            'status': forms.HiddenInput()  # optionally hide if always True
        }

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['assignedDoctor'].queryset = Doctor.objects.filter(status=True)
        self.fields['assignedDoctor'].empty_label = "Select Doctor (Name & Department)"


        
        
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model= Doctor
        fields=['address','mobile','department','status','profile_pic']
        
class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.filter(status=True),empty_label="Doctor Name and Department")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.filter(status=True),empty_label="Patient Name and Symptoms")
    
    class Meta:
        model=models.Appointment
        fields = ['doctorId', 'patientId', 'description', 'status']    
            
class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    
    class Meta:
        model=models.Appointment
        fields=['description','status']
        
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
    
    
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription']
        widgets = {
            'prescription': forms.Textarea(attrs={'rows': 3, 'cols': 30}),
        }