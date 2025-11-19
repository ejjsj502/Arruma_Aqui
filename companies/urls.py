from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('', views.list_companies, name='list'),
    path('search/', views.search_companies, name='search'),
    path('<int:user_id>/', views.detail_company, name='detail'),
    path('review/delete/<int:pk>/', views.delete_review, name='delete_review'),

    # NOVAS URLs para respostas
    path('review/respond/<int:pk>/', views.respond_to_review, name='respond_review'),
    path('review/response/edit/<int:pk>/', views.edit_response, name='edit_response'),
    path('review/response/delete/<int:pk>/', views.delete_response, name='delete_response'),

    # URLs para orçamentos
    path('budget/request/<int:user_id>/', views.request_budget, name='request_budget'),
    path('budgets/', views.budget_requests, name='budget_requests'),
    path('budget/<int:pk>/', views.budget_detail, name='budget_detail'),
    path('budget/respond/<int:pk>/', views.respond_budget, name='respond_budget'),
    path('budget/client-respond/<int:pk>/', views.client_respond_budget, name='client_respond_budget'),
    path('budget/cancel/<int:pk>/', views.cancel_budget, name='cancel_budget'),
]