from django import forms
from .models import Review
from .models import BudgetRequest
from datetime import datetime

class ClientResponseForm(forms.ModelForm):
    ACCEPTANCE_CHOICES = [
        ('accepted', 'Aceitar Orçamento'),
        ('rejected', 'Recusar Orçamento'),
    ]
    
    acceptance = forms.ChoiceField(
        choices=ACCEPTANCE_CHOICES,
        widget=forms.RadioSelect,
        label='Decisão'
    )
    
    class Meta:
        model = BudgetRequest
        fields = ['client_response']
        widgets = {
            'client_response': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Digite sua resposta para o prestador (opcional)...',
                'class': 'form-control'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        acceptance = cleaned_data.get('acceptance')
        client_response = cleaned_data.get('client_response')
        
        if acceptance == 'rejected' and not client_response:
            raise forms.ValidationError('Por favor, explique o motivo da recusa para o prestador.')
        
        return cleaned_data

class BudgetRequestForm(forms.ModelForm):
    class Meta:
        model = BudgetRequest
        fields = ['service_description', 'photos', 'desired_date', 'urgency']
        widgets = {
            'service_description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva detalhadamente o serviço que precisa...',
                'class': 'form-control'
            }),
            'desired_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': datetime.now().strftime('%Y-%m-%d')
            }),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'photos': forms.FileInput(attrs={'class': 'form-control'})
        }
    
    def clean_desired_date(self):
        desired_date = self.cleaned_data.get('desired_date')
        if desired_date < datetime.now().date():
            raise forms.ValidationError('A data desejada não pode ser no passado.')
        return desired_date

class BudgetResponseForm(forms.ModelForm):
    class Meta:
        model = BudgetRequest
        fields = ['status', 'company_response', 'proposed_price']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'company_response': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Digite sua resposta para o cliente...',
                'class': 'form-control'
            }),
            'proposed_price': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        proposed_price = cleaned_data.get('proposed_price')
        company_response = cleaned_data.get('company_response')
        
        if status == 'accepted' and not proposed_price:
            raise forms.ValidationError('É necessário informar o preço quando aceitar um orçamento.')
        
        if status != 'pending' and not company_response:
            raise forms.ValidationError('É necessário fornecer uma resposta para o cliente.')
        
        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Deixe seu comentário sobre o serviço...',
                'class': 'form-control'
            }),
            'rating': forms.Select(attrs={'class': 'form-control'})
        }


# NOVO FORM: Para resposta da empresa
class CompanyResponseForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['company_response']
        widgets = {
            'company_response': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Digite sua resposta para o cliente...',
                'class': 'form-control'
            })
        }