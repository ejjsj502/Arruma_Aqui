from django.contrib import admin
from .models import Review
from .models import BudgetRequest

@admin.register(BudgetRequest)
class BudgetRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'company', 'status', 'urgency', 'desired_date', 'created_at']
    list_filter = ['status', 'urgency', 'created_at']
    search_fields = ['client__username', 'company__user__name', 'service_description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'client_name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['company__user__name', 'client__username']
    
    def company_name(self, obj):
        return obj.company.user.name
    company_name.short_description = 'Empresa'
    
    def client_name(self, obj):
        return obj.client.username
    client_name.short_description = 'Cliente'

