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
    class Meta:
        model = Client  # Muda para Client
        fields = ['cpf', 'tel', 'city']  # Campos do Client

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona campos do User se necessário
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['name'] = forms.CharField(
                initial=self.instance.user.name, 
                required=True
            )
            self.fields['email'] = forms.EmailField(
                initial=self.instance.user.email, 
                required=True
            )

    @transaction.atomic
    def save(self, commit=True):
        client = super().save(commit=False)
        
        # Atualiza campos do User
        if hasattr(self, 'cleaned_data'):
            if 'name' in self.cleaned_data:
                client.user.name = self.cleaned_data['name']
            if 'email' in self.cleaned_data:
                client.user.email = self.cleaned_data['email']
            client.user.save()
        
        if commit:
            client.save()
        
        return client.user

class UpdateCompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company  # Muda para Company
        fields = ['logoURL', 'cnpj', 'tel', 'job', 'city']  # Campos do Company

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona campos do User se necessário
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['name'] = forms.CharField(
                initial=self.instance.user.name, 
                required=True
            )
            self.fields['email'] = forms.EmailField(
                initial=self.instance.user.email, 
                required=True
            )

    @transaction.atomic
    def save(self, commit=True):
        company = super().save(commit=False)
        
        # Atualiza campos do User
        if hasattr(self, 'cleaned_data'):
            if 'name' in self.cleaned_data:
                company.user.name = self.cleaned_data['name']
            if 'email' in self.cleaned_data:
                company.user.email = self.cleaned_data['email']
            company.user.save()
        
        if commit:
            company.save()
        
        return company.user
        
        