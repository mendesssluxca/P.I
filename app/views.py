# Importações Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.views import View

# Importações de Form.py
from .form import (
    CustomUserCreationForm,
    FlashcardForm,
    TopicoForm,
    UserProfileForm,
    FileUploadForm
    )

# Importação de Models.py
from .models import (
    Usuario,
    Flashcard,
    Topico,
    FileUpload
    )

# Index
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

@login_required
def indexlogado(request):
    return render(request, 'indexlogado.html')

# Página Sobre
def sobre(request):
    return render(request, 'sobre.html')

#Página Perfil
@login_required
def editar_senha(request):
    user = request.user  
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 and password2 and password1 == password2:
            user.set_password(password1) 
            user.save() 
            update_session_auth_hash(request, user) 
            messages.success(request, 'Senha alterada com sucesso!') 
            return redirect('perfil') 
        else:
            messages.error(request, 'As senhas não coincidem.') 

    return render(request, 'perfil/editar_senha.html', {'user': user}) 

@login_required
def excluir_conta(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.delete()  
            messages.success(request, "Sua conta foi excluída com sucesso.")
            return redirect('/') 
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao excluir sua conta: {e}")
            return redirect('perfil/perfil')

    return redirect('/')

@login_required
def editar_perfil(request):
    usuario = request.user.usuario  
    user = request.user 

    if request.method == "POST":
        if 'nome' in request.POST:
            usuario.nome = request.POST['nome']
        if 'datanasc' in request.POST:
            usuario.datanasc = request.POST['datanasc']
        if 'cpf' in request.POST:
            usuario.cpf = request.POST['cpf']
        
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save() 
        
        usuario.save() 
        return redirect('perfil') 

    return render(request, 'perfil/editar_perfil.html', {'usuario': usuario, 'user': user})

@login_required
def perfil(request):
    usuario = request.user.usuario  

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=usuario)  
        if form.is_valid():
            form.save()  
            return redirect('perfil') 
    else: 
        form = UserProfileForm(instance=usuario)  

    return render(request, 'perfil/perfil.html', {'form': form, 'usuario': usuario})


# Registro de Usuário
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automaticamente após o registro
            return redirect('perfil')  # Redireciona para a página de perfil após o registro
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})



# Flashcards Views
@login_required
def listar_flashcards(request):
    search_query = request.GET.get('search')
    if search_query:
        flashcards = Flashcard.objects.filter(usuario=request.user, topico__icontains=search_query)
    else:
        flashcards = Flashcard.objects.filter(usuario=request.user)
    return render(request, 'flashcards/listar_flashcards.html', {'flashcards': flashcards})

@login_required
def criar_flashcard(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.usuario = request.user  # Associa ao usuário logado
            flashcard.save()
            return redirect('listar_flashcards')
    else:
        form = FlashcardForm()
    return render(request, 'flashcards/criar_flashcard.html', {'form': form})

@login_required
def editar_flashcard(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk, usuario=request.user)  #
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('listar_flashcards')
    else:
        form = FlashcardForm(instance=flashcard)
    return render(request, 'flashcards/editar_flashcard.html', {'form': form, 'flashcard': flashcard})

@login_required
def excluir_flashcard(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk, usuario=request.user)  # Verifica se o usuário é o dono
    if request.method == 'POST':
        flashcard.delete()
        return redirect('listar_flashcards')
    return render(request, 'flashcards/excluir_flashcard.html', {'flashcard': flashcard})


# Tópicos Views
@login_required
def criar_topico(request):
    if request.method == "POST":
        form = TopicoForm(request.POST)
        if form.is_valid():
            topico = form.save(commit=False)
            topico.owner = request.user  # Define o usuário como owner
            topico.save() 
            return redirect('listar_topicos') 
    else:
        form = TopicoForm()
    return render(request, 'topicos/criar_topico.html', {'form': form})



@login_required
def listar_topicos(request):
    if request.user.is_staff:
        topicos = Topico.objects.all()  # Administradores veem todos
    else:
        topicos = Topico.objects.filter(owner=request.user)  # Usuários veem apenas seus próprios tópicos
    
    return render(request, 'topicos/listar_topicos.html', {'topicos': topicos})


@login_required
def editar_topico(request, topico_id):
    topico = get_object_or_404(Topico, id_topico=topico_id)

    # Verifica se o usuário é o proprietário ou um administrador
    if topico.owner != request.user and not request.user.is_staff:
        return render(request, '403.html')  # Página de acesso negado

    if request.method == 'POST':
        form = TopicoForm(request.POST, instance=topico)
        if form.is_valid():
            form.save()
            return redirect('listar_topicos')
    else:
        form = TopicoForm(instance=topico)
    return render(request, 'topicos/editar_topico.html', {'form': form, 'topico': topico})

@login_required
def excluir_topico(request, topico_id):
    topico = get_object_or_404(Topico, id_topico=topico_id)

    # Verifica se o usuário é o proprietário ou um administrador
    if topico.owner != request.user and not request.user.is_staff:
        return render(request, '403.html')  # Página de acesso negado

    if request.method == 'POST':
        topico.delete()
        return redirect('listar_topicos')
    return render(request, 'topicos/excluir_topico.html', {'topico': topico})

@login_required
def visualizar_topico(request, topico_id):
    topico = get_object_or_404(Topico, id_topico=topico_id)

    # Verifica se o usuário é o proprietário ou um administrador
    if topico.owner != request.user and not request.user.is_staff:
        return render(request, '403.html')  # Página de acesso negado ou redireciona

    flashcards = topico.flashcard_set.all()  
    return render(request, 'topicos/visualizar_topico.html', {'topico': topico, 'flashcards': flashcards})


#Arquivos
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_upload = form.save(commit=False)
            file_upload.usuario = request.user  # Define o usuário atual como o dono do arquivo
            file_upload.save()
            return redirect('lista_uploads')
    else:
        form = FileUploadForm()
    return render(request, 'arquivos_upload/upload_file.html', {'form': form})

@login_required
def lista_uploads(request):
    if request.user.is_superuser:
        arquivos = FileUpload.objects.all()  # Admin pode ver todos
    else:
        arquivos = FileUpload.objects.filter(usuario=request.user)  # Usuário vê apenas os próprios uploads
    return render(request, 'arquivos_upload/lista_uploads.html', {'arquivos': arquivos})

@login_required
def deletar_arquivo(request, pk):
    arquivo = get_object_or_404(FileUpload, pk=pk, usuario=request.user)
    if request.method == 'POST':
        arquivo.delete()
        return redirect('lista_uploads')
    return render(request, 'arquivos_upload/confirm_delete.html', {'arquivo': arquivo})

@login_required
def editar_arquivo(request, pk):
    arquivo = get_object_or_404(FileUpload, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, instance=arquivo)
        if form.is_valid():
            form.save()
            return redirect('lista_uploads')
    else:
        form = FileUploadForm(instance=arquivo)

    return render(request, 'arquivos_upload/editar_arquivo.html', {'form': form, 'arquivo': arquivo})