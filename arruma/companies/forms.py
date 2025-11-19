from django import forms
from .models import Review, ReviewReport

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


class ReviewReportForm(forms.ModelForm):
    class Meta:
        model = ReviewReport
        fields = ['reason', 'description']
        widgets = {
            'reason': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-secondary'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva o motivo da denúncia (opcional)',
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-secondary focus:border-secondary'
            })
        }
        labels = {
            'reason': 'Motivo da denúncia',
            'description': 'Descrição adicional (opcional)'
        }