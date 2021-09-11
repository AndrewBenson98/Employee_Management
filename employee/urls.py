from django.urls import path
from . import views

urlpatterns = [
    path('', views.employeeList, name='employeeList'),
    path('emp/<str:pk>', views.emp_profile, name='emp_profile'),
    path('emp/new/', views.emp_new, name='emp_new'),
    path('emp/<str:pk>/edit/', views.emp_edit, name='emp_edit'),
    path('emp/<str:pk>/remove/', views.emp_remove, name='emp_remove'),
    path('login/', views.login_request, name='login'),
]