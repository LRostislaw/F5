from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='home'),
]


urlpatterns += [
    path('signup', views.RegisterFormView.as_view(), name='signup'),
    path('login', views.LoginFormView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='login'),
    path('edit_password', views.ChangeFormView.as_view(), name='edit_password'),
    path('statistic', views.statistic, name='statistic'),
    path('settings', views.settings, name='settings'),
    path('home', views.index, name='home'),
]