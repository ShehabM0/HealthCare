from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('create-card/', views.CreateCard, name='create-new-credit-card'),

    path('neglect-card/<int:pk>/', views.NeglectCard, name='neglect-credit-card-for-user'),
    path('neglect-cards/', views.NeglectCards, name='neglect-all-credit-cards-for-user'),
    path('assign-card/', views.AssignCard, name='assign-credit-card-for-user'),
    path('list-cards/', views.ListCards, name='list-user-credit-cards'),

    path('list-purchases/', views.ListPurchases, name='list-purchase'),
    path('add-purchase/', views.AddPurchase, name='add-purchase'),
]