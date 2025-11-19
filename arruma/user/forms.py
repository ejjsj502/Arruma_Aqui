from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Company,Client

class ClientSignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    cpf = forms.CharField(required=True)
    tel = forms.CharField(required=True)
    city = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.name = self.cleaned_data.get('name')
        user.save()
        client = Client.objects.create(user=user)
        client.tel=self.cleaned_data.get('tel')
        client.city=self.cleaned_data.get('city')
        client.cpf=self.cleaned_data.get('cpf')
        client.save()
        return user

class CompanySignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    logoURL = forms.CharField(required=True)
    cnpj = forms.CharField(required=True)
    tel = forms.CharField(required=True)
    job = forms.CharField(required=True)
    city = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.name = self.cleaned_data.get('name')
        user.save()
        company = Company.objects.create(user=user)
        company.tel=self.cleaned_data.get('tel')
        company.logoURL=self.cleaned_data.get('logoURL')
        company.cnpj=self.cleaned_data.get('cnpj')
        company.city=self.cleaned_data.get('city')
        company.job=self.cleaned_data.get('job')
        company.save()
        return user

class UpdateClientProfileForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Nome completo')

    class Meta:
        model = Client
        fields = ['cpf', 'tel', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['name'].initial = self.instance.user.name

        for field_name in ['cpf', 'tel']:
            self.fields[field_name].widget = forms.TextInput(attrs={'inputmode': 'numeric'})

    @transaction.atomic
    def save(self, commit=True):
        client = super().save(commit=False)
        client.user.name = self.cleaned_data['name']
        if commit:
            client.user.save(update_fields=['name'])
            client.save()
        return client


class UpdateCompanyProfileForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Nome da empresa')

    class Meta:
        model = Company
        fields = ['logoURL', 'cnpj', 'tel', 'job', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['name'].initial = self.instance.user.name

        for numeric in ['cnpj', 'tel']:
            self.fields[numeric].widget = forms.TextInput(attrs={'inputmode': 'numeric'})

    @transaction.atomic
    def save(self, commit=True):
        company = super().save(commit=False)
        company.user.name = self.cleaned_data['name']
        if commit:
            company.user.save(update_fields=['name'])
            company.save()
        return company
        
        