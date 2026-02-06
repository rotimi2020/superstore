from django.urls import path
from . import views

app_name = 'superstore_app'

urlpatterns = [
    
    # =========================
    # USER DASHBOARD ROUTES
    # =========================    
    path('', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('sales/', views.sales, name='sales'),

]
