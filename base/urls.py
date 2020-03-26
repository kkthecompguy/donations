from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
  path('', views.HomeView.as_view(), name='index'),
  path('charge/', views.ChargeView.as_view(), name='charge'),
  path('success/<str:args>/', views.success_msg, name='success')
]