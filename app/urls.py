from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastroGato/', views.cadastroGato, name='cadastroGato'),
    path('gatos/', views.gatos, name='gatos'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('editar_usuario/<int:id_usuario>',views.editar_usuario, name="editar_usuario"),
    path('excluir_usuario/<int:id_usuario>',views.excluir_usuario, name="excluir_usuario"),
    path('exibir_usuario/',views.exibir_usuario, name="exibir_usuario"),
    path('galeria/',views.mostrar_fotos, name="galeria"),
    path('criar_foto/',views.criar_foto, name="criar_foto"),
    path('grafico/', views.grafico, name='grafico'),
    path('adocao/<int:gato_id>/', views.adocao, name='adocao'),
] 