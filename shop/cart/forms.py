from .models import Customer
from django import forms


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ('pk',)
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your lastname'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your company name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your email'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your state'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter address'
            }),
            'town': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter town'
            }),
             'zip_code': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter zip code'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your phone number'
            }),

            'comment': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter comment'
            }),



        }