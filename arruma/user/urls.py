from django.urls import path
from .import  views

urlpatterns=[
     path('register/',views.register, name='register'),
     path('client_register/',views.customer_register.as_view(), name='client_register'),
     path('company_register/',views.employee_register.as_view(), name='company_register'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('profile/<int:user_id>/',views.profile_client, name='profile'),
     path('update_client_profile/<int:user_id>/',views.UpdateClientProfile.as_view(), name='update_client_profile'),
     path('update_company_profile/<int:user_id>/',views.UpdateCompanyProfile.as_view(), name='update_company_profile'),
]