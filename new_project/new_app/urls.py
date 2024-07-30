from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from new_app.views import CustomPasswordResetView

urlpatterns=[
    path("", views.index, name="index"),
    path("buy_data/", views.data_purchase, name="data_purchase"),
    path('register/', views.register_user, name = 'register'),
    path('login/', views.user_login, name = 'user_login'),
    path('signout/', views.signout, name ='signout'), 
    path('profile/', views.profile, name ='profile'), 
    path('update_profile/', views.update_profile, name = 'update_profile'), 
    path('change_password/', views.change_password, name = 'change_password'),
    path('switch_pdt/', views.switch_pdt, name = 'switch_pdt'),
    path('data_of/<int:id>/', views.data_of, name = 'data_of'),
    path('data_on/<int:id>/', views.data_on, name = 'data_on'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),



    path('webhook/', views.webhook, name = 'webhook'),
    path('ajax/load-data-types/', views.ajax_load_data_types, name='ajax_load_data_types'),
    path('ajax/load-data-plans/', views.ajax_load_data_plans, name='ajax_load_data_plans'),


    path('password_reset/', CustomPasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

]
