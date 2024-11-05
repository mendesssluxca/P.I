from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from app import views
from app.views import (
    listar_topicos,
    criar_topico,
    editar_topico,
    excluir_topico,
    visualizar_topico,
    editar_perfil, 
    editar_senha, 
    excluir_conta

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls")),
   
    # URLs de autenticação
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # URLs de registro e página inicial logada
    path('register/', views.register, name='register'),
    path('indexlogado/', views.indexlogado, name='indexlogado'),
    
    # URL sobre
    path('sobre/', views.sobre, name='sobre'),

    # URLs de Flashcards
    path('flashcards/', views.listar_flashcards, name='listar_flashcards'),
    path('flashcards/criar/', views.criar_flashcard, name='criar_flashcard'),
    path('flashcards/<int:pk>/editar/', views.editar_flashcard, name='editar_flashcard'), 
    path('flashcards/<int:pk>/excluir/', views.excluir_flashcard, name='excluir_flashcard'),  

    #URLs de Tópicos
    path('topicos/', listar_topicos, name='listar_topicos'),
    path('topicos/criar/', criar_topico, name='criar_topico'),
    path('topicos/<int:topico_id>/', visualizar_topico, name='visualizar_topico'),
    path('topicos/<int:topico_id>/editar/', editar_topico, name='editar_topico'),
    path('topicos/<int:topico_id>/excluir/', excluir_topico, name='excluir_topico'),

    #URLs de Perfil
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),  
    path('perfil/editar_senha/', editar_senha, name='editar_senha'),  
    path('perfil/excluir_conta/', excluir_conta, name='excluir_conta'),  

    #Arquivos Upload
    path('upload/', views.upload_file, name='upload_file'),
    path('uploads/', views.lista_uploads, name='lista_uploads'),
    path('uploads/deletar/<int:pk>/', views.deletar_arquivo, name='deletar_arquivo'),
    path('editar_arquivo/<int:pk>/', views.editar_arquivo, name='editar_arquivo'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
