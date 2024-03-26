from django.urls import path
from . import views

app_name = 'verification_code'

urlpatterns = [
    path('send/change-email/', views.CreateVerificationCode, name = 'create-verification-code-update-email'),
    path('send/register/', views.CreateVerificationCode, name = 'create-verification-code-registration'),

    path('list/', views.ListVerificationCodes, name = 'list-verification-codes'),

    path('verify/', views.VerifyCode, name = 'veify-code'),
]

