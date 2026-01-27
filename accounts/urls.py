from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Importamos as views prontas do Django

urlpatterns = [
    # Rotas Normais
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('mensagens/', views.ver_leads, name='ver_leads'),

    # --- FLUXO DE RECUPERAÇÃO DE SENHA (4 Etapas) ---
    
    # 1. Tela "Esqueci minha senha" (Digita o email)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    
    # 2. Tela "Email enviado" (Feedback pro usuário)
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    
    # 3. Tela "Nova Senha" (Link que chega no email)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    
    # 4. Tela "Sucesso" (Senha alterada)
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]