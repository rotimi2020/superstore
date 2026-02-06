from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('login/', views.staff_login, name='staff_login'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('sales/', views.staff_sales_list, name='staff_sales_list'),
    path('sales/add/', views.staff_sales_create, name='staff_sales_create'),
    path('sales/<int:pk>/', views.staff_sales_detail, name='staff_sales_detail'),
    path('sales/<int:pk>/edit/', views.staff_sales_update, name='staff_sales_update'),
    path('sales/<int:pk>/delete/', views.staff_sales_delete, name='staff_sales_delete'),
]
