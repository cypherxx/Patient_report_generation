from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', views.sign_in, name="sign_in"),
    path('dashboard/', views.index, name="index"),
    path('sign_out/',views.sign_out,name='sign_out'),
    path('register/',views.register,name='register'),
    path('profile/',views.user_profile,name='profile'),
    path('search_report/',views.Search_report,name='search_report'),
    path('edit/',views.edit,name='edit'),
    path('get_report/',views.get_report.as_view(),name='get_report'),
    path('new_profile/',views.new_profile.as_view(),name='new_profile'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='html/password_reset.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='html/password_resent_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='html/password_reset_form.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='html/password_reset_done.html'),name='password_reset_complete'),
    path('verify/', views.verify, name="verify"),
    path('detail/',views.detail,name='detail'),
    path('update_detail/',views.update_detail,name='update_detail'),
    path('sendmail/<pk>/',views.send_report_mail,name='send_mail'),
    path('report_mail/<pk>',views.report_mail,name='report_mail'),
    path('delete/<pk>',views.delete_report,name='delete_report')
    
]