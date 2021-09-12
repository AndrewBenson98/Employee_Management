from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('employee_list', views.employee_list, name='employee_list'),
    path('emp/<str:pk>', views.emp_profile, name='emp_profile'),
    path('emp/new/', views.emp_new, name='emp_new'),
    path('emp/<str:pk>/edit/', views.emp_edit, name='emp_edit'),
    path('emp/<str:pk>/remove/', views.emp_remove, name='emp_remove'),
    path('login/', views.login_request, name='login_request'),
    path('logout/', views.logout_request, name='logout_request'),
    path('profile/', views.user_profile, name='user_profile'),
    path('leave/request', views.leave_request, name='leave_request'),
    path('leave/list', views.leave_list, name='leave_list'),
    path('leave/detail/<int:pk>', views.leave_detail, name='leave_detail'),
    path('leave/detail/<int:pk>/approve', views.leave_approve, name='leave_approve'),
    path('leave/detail/<int:pk>/reject', views.leave_reject, name='leave_reject'),
]