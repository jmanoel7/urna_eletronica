from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name = 'usuarios/form.html'
    ), name='login'),
    path('', views.usuarios, name='index'),
    path('gerente/', views.gerente, name='gerente'),
    path('assistente/', views.assistente, name='assistente'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
