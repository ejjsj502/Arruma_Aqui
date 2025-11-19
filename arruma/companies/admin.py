from django.contrib import admin
from .models import Review, ReviewReport

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


@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ['review_info', 'reporter_name', 'reason', 'status', 'created_at']
    list_filter = ['status', 'reason', 'created_at']
    search_fields = ['review__client__username', 'reporter__username', 'description']
    readonly_fields = ['created_at', 'reviewed_at']
    actions = ['mark_as_reviewed', 'mark_as_resolved', 'mark_as_dismissed']
    
    fieldsets = (
        ('Informações da Denúncia', {
            'fields': ('review', 'reporter', 'reason', 'description', 'status')
        }),
        ('Revisão', {
            'fields': ('reviewed_by', 'reviewed_at'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def review_info(self, obj):
        return f"Avaliação #{obj.review.id} - {obj.review.client.username}"
    review_info.short_description = 'Avaliação Denunciada'
    
    def reporter_name(self, obj):
        return obj.reporter.username
    reporter_name.short_description = 'Denunciante'
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed', reviewed_by=request.user)
        self.message_user(request, f'{queryset.count()} denúncia(s) marcada(s) como revisada(s).')
    mark_as_reviewed.short_description = 'Marcar como revisadas'
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved', reviewed_by=request.user)
        self.message_user(request, f'{queryset.count()} denúncia(s) marcada(s) como resolvida(s).')
    mark_as_resolved.short_description = 'Marcar como resolvidas'
    
    def mark_as_dismissed(self, request, queryset):
        queryset.update(status='dismissed', reviewed_by=request.user)
        self.message_user(request, f'{queryset.count()} denúncia(s) marcada(s) como descartada(s).')
    mark_as_dismissed.short_description = 'Marcar como descartadas'
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data and obj.status != 'pending':
            if not obj.reviewed_by:
                obj.reviewed_by = request.user
            from django.utils import timezone
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

