from django.urls import path
#from .views import register, dashboard, user_login, user_logout
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
    
    LoginView,
    LogoutView,
   
)
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='autho/login.html', redirect_authenticated_user=True, next_page='dashboard'),  name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('forget_password/', PasswordResetView.as_view(template_name='autho/forget_password.html', email_template_name='password_reset_email.html'), name='password_reset'),
    path('forget_password/done/', PasswordResetDoneView.as_view(template_name='autho/forget_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='autho/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='autho/password_reset_complete.html'), name='password_reset_complete'),


    path('change_password/', PasswordChangeView.as_view(template_name='autho/change_password.html'), name='password_change'),
    path('change_password/done/', PasswordChangeDoneView.as_view(template_name='autho/change_password_done.html'), name='password_change_done'),

    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),


    path('company/', views.company_list, name='company_list'),
    path('company/create/', views.company_create, name='company_create'),
    path('company/update/<int:pk>/', views.company_update, name='company_update'),
    path('company/delete/<int:pk>/', views.company_delete, name='company_delete'),

 
    path('job/', views.job_list, name='job_list'),
    path('job/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/update/<int:pk>/', views.job_update, name='job_update'),
    path('job/delete/<int:pk>/', views.job_delete, name='job_delete'),

    path('job/apply/<int:pk>/', views.apply_job, name='apply_job'),
    path('job/available/', views.available_jobs, name='available_jobs'),
    
    path('job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),

    path('applicant/', views.applicant_list, name='applicant_list'),
    path('applicant/create/', views.applicant_create, name='applicant_create'),
    path('applicant/update/<int:pk>/', views.applicant_update, name='applicant_update'),
    path('applicant/delete/<int:pk>/', views.applicant_delete, name='applicant_delete'),



    path('contact/', views.contact_us, name='contact_us'),
    path('about_us/', views.about_us, name='about_us'),
    path('job_page/', views.jobpage, name='job_page'),
]

