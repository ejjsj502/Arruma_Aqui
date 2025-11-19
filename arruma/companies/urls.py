from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('', views.list_companies, name='list'),
    path('search/', views.search_companies, name='search'),
    path('<int:user_id>/', views.detail_company, name='detail'),
    path('review/delete/<int:pk>/', views.delete_review, name='delete_review'),
    path('review/report/<int:pk>/', views.report_review, name='report_review'),
]