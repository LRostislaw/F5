from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='home'),
]


urlpatterns += [
    path('signup', views.RegisterFormView.as_view(), name='signup'),
    path('signup/activate/<str:sign>/', views.user_activate, name='signup_activate'),
    path('choice/doctor/<str:sign>/<str:email>/', views.choice_doctor, name='choice_doctor'),
    path('signup/done', views.SignupDoneView.as_view(), name='signup_done'),
    path('login', views.LoginFormView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('edit_password', views.ChangeFormView.as_view(), name='edit_password'),
    path('statistic', views.statistic, name='statistic'),
    path('settings', views.Settings.as_view(), name='settings'),
    path('home', views.index, name='home'),
    path('privacy', views.privacy, name='privacy'),
]