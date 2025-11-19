from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Péssimo'),
        (2, '2 - Ruim'),
        (3, '3 - Regular'),
        (4, '4 - Bom'),
        (5, '5 - Excelente'),
    ]
    
    company = models.ForeignKey('user.Company', on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # CORREÇÃO AQUI
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['company', 'client']
    
    def __str__(self):
        return f"Avaliação de {self.client.username} para {self.company.user.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Atualizar a média da empresa
        self.company.update_ratings()


class ReviewReport(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam ou conteúdo promocional'),
        ('inappropriate', 'Conteúdo inadequado ou ofensivo'),
        ('false', 'Informação falsa ou enganosa'),
        ('harassment', 'Assédio ou bullying'),
        ('other', 'Outro motivo'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('reviewed', 'Revisado'),
        ('resolved', 'Resolvido'),
        ('dismissed', 'Descartado'),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True, help_text='Descreva o motivo da denúncia (opcional)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reports_reviewed'
    )
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['review', 'reporter']  # Um usuário só pode denunciar o mesmo review uma vez
    
    def __str__(self):
        return f"Denúncia de {self.reporter.username} sobre avaliação #{self.review.id}"