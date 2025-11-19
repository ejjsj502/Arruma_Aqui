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


    company_response = models.TextField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)
    
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
    
    def can_respond(self, user):
        """Verifica se o usuário pode responder a esta avaliação"""
        return user == self.company.user



class BudgetRequest(models.Model):
    URGENCY_CHOICES = [
        ('low', 'Baixa (1-2 semanas)'),
        ('medium', 'Média (3-7 dias)'),
        ('high', 'Alta (1-2 dias)'),
        ('emergency', 'Emergência (24 horas)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),           # Aguardando resposta do prestador
        ('quoted', 'Orçado'),              # Prestador enviou orçamento
        ('accepted', 'Aceito'),            # Cliente aceitou o orçamento
        ('rejected', 'Recusado'),          # Cliente recusou o orçamento
        ('cancelled', 'Cancelado'),        # Cancelado por qualquer parte
    ]
    
    # Relações
    company = models.ForeignKey('user.Company', on_delete=models.CASCADE, related_name='budget_requests')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budget_requests')
    
    # Dados do serviço
    service_description = models.TextField(verbose_name='Descrição do serviço')
    photos = models.ImageField(upload_to='budget_photos/', blank=True, null=True, verbose_name='Fotos')
    desired_date = models.DateField(verbose_name='Data desejada')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium', verbose_name='Urgência')
    
    # Resposta do prestador
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    company_response = models.TextField(blank=True, null=True, verbose_name='Resposta do prestador')
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Preço proposto')
    response_date = models.DateTimeField(blank=True, null=True)
    
    # Resposta do cliente ao orçamento
    client_response = models.TextField(blank=True, null=True, verbose_name='Resposta do cliente')
    client_response_date = models.DateTimeField(blank=True, null=True)
    
    # Datas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Solicitação de Orçamento'
        verbose_name_plural = 'Solicitações de Orçamento'
    
    def __str__(self):
        return f"Orçamento #{self.id} - {self.client.username} para {self.company.user.name}"
    
    def can_respond(self, user):
        """Verifica se o usuário pode responder a este orçamento"""
        return user == self.company.user and self.status == 'pending'
    
    def can_accept_reject(self, user):
        """Verifica se o cliente pode aceitar/recusar o orçamento"""
        return user == self.client and self.status == 'quoted'
    
    def can_cancel(self, user):
        """Verifica se o usuário pode cancelar este orçamento"""
        return (user == self.client or user == self.company.user) and self.status in ['pending', 'quoted']
    
    def get_urgency_color(self):
        """Retorna cor baseada na urgência"""
        colors = {
            'low': 'green',
            'medium': 'blue', 
            'high': 'orange',
            'emergency': 'red'
        }
        return colors.get(self.urgency, 'gray')