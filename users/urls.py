from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.ListUsers, name = 'list-all-users'),
    path('list/<str:type>/', views.ListUsers, name = 'list-users-by-type'),

    path('get-user/<int:pk>/', views.GetUser, name = 'get-user-by-id'),
    path('get-current-user/', views.GetCurrentUser, name = 'get-current-logged-in-user'),

    path('update/<int:pk>/', views.UpdateUser, name = 'update-user-profile'),     #TODO Authorization
    path('update/', views.UpdateUser, name = 'update-currentuser-profile'),

    path('delete/<int:pk>/', views.DeleteUser, name = 'delete-user'),     #TODO Authorization
    path('delete/', views.DeleteUser, name = 'delete-current-logged-in-user'),

    path('update-email/', views.UpdateEmail, name = 'update-currentuser-email'),
    path('update-password/', views.UpdatePassword, name = 'update-currentuser-password'),

    path('forgot-password/', views.ForgotPassword, name = 'currentuser-forgot-password'),
    path('reset-password/<str:token>/', views.ResetPassword, name = 'currentuser-reset-password'),
    
]

