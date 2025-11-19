from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('como-funciona/', views.how_it_works, name='how_it_works'),
    path('termos-de-uso/', views.terms_of_use, name='terms_of_use'),
    path('politica-de-privacidade/', views.privacy_policy, name='privacy_policy'),
]