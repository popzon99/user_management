from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'role', 'country', 'nationality', 'mobile', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['role'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['nationality'].widget.attrs['class'] = 'form-control'
        self.fields['mobile'].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

       
        if role == 'student':
           
            mobile = cleaned_data.get('mobile')
            if not mobile:
                raise ValidationError('Mobile number is required for the student role.')

        elif role == 'staff':
            
            staff_name = cleaned_data.get('name')
            if not staff_name:
                raise ValidationError('Staff member name is required.')

        elif role == 'admin':
        
            country = cleaned_data.get('country')
            nationality = cleaned_data.get('nationality')
            if not country or not nationality:
                raise ValidationError('Both country and nationality are required for the admin role.')

        elif role == 'editor':
         
            editor_email = cleaned_data.get('email')
            if not editor_email.endswith('@yourdomain.com'):
                raise ValidationError('Editor email must be from yourdomain.com.')

     

        return cleaned_data
