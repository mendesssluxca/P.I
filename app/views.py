# Importações Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.db.models import Q
from django.contrib import messages
from django.views import View

# Importações de Form.py
from .form import (
    CustomUserCreationForm,
    FlashcardForm,
    TopicoForm,
    UserProfileForm,
    DuvidaForm,
    ComentarioForm,
    )

# Importação de Models.py
from .models import (
    Usuario,
    Flashcard,
    Topico,
    Duvida,
    Comentario
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

def perfil(request):
    if request.user.is_authenticated:
        try:
            # Tente acessar o objeto Usuario relacionado ao User
            usuario = request.user.usuario
            usuario_nao_encontrado = False
        except Usuario.DoesNotExist:
            # Caso não exista, defina a variável para mostrar que o superusuário não tem um 'usuario'
            usuario = None
            usuario_nao_encontrado = True

        return render(request, 'perfil/perfil.html', {
            'usuario': usuario,
            'usuario_nao_encontrado': usuario_nao_encontrado
        })
    else:
        return redirect('login')



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
        # Admins veem todos os tópicos disponíveis no sistema
        topicos = Topico.objects.filter(disponivel_no_sistema=True)
    else:
        # Usuários veem tópicos próprios e também os do sistema
        topicos = Topico.objects.filter(
            Q(owner=request.user) | Q(disponivel_no_sistema=True)
        )
    
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


@login_required
def lista_duvidas(request):
    duvidas = Duvida.objects.all()
    return render(request, 'forum/lista_duvidas.html', {'duvidas': duvidas})

@login_required
def detalhes_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)
    comentarios = duvida.comentarios.all()
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentarios = duvida.comentarios.order_by('-data_criacao')
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.duvida = duvida
            comentario.save()
            return redirect('detalhes_duvida', id=duvida.id)
    else:
        form = ComentarioForm()
    return render(request, 'forum/detalhes_duvida.html', {'duvida': duvida, 'comentarios': comentarios, 'form': form})

@login_required
def cria_duvida(request):
    if request.method == 'POST':
        form = DuvidaForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            if Duvida.objects.filter(titulo=titulo).exists():
                messages.error(request, "Já existe uma dúvida com esse título.")
                return render(request, 'forum/cria_duvida.html', {'form': form})
            duvida = form.save(commit=False)
            duvida.autor = request.user
            duvida.save()
            messages.success(request, "Dúvida criada com sucesso!")
            return redirect('lista_duvidas')
    else:
        form = DuvidaForm()
    return render(request, 'forum/cria_duvida.html', {'form': form})

@login_required
def edita_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)
    if request.user != duvida.autor and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para editar esta dúvida.")
        return redirect('detalhes_duvida', id=duvida.id)
    if request.method == 'POST':
        form = DuvidaForm(request.POST, instance=duvida)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            if Duvida.objects.exclude(id=duvida.id).filter(titulo=titulo).exists():
                messages.error(request, "Já existe uma dúvida com esse título.")
                return render(request, 'forum/edita_duvida.html', {'form': form, 'duvida': duvida})
            form.save()
            messages.success(request, "Dúvida atualizada com sucesso!")
            return redirect('detalhes_duvida', id=duvida.id)
    else:
        form = DuvidaForm(instance=duvida)
    return render(request, 'forum/edita_duvida.html', {'form': form, 'duvida': duvida})

@login_required
def exclui_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)
    if request.user != duvida.autor and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para excluir esta dúvida.")
        return redirect('detalhes_duvida', id=duvida.id)
    if request.method == 'POST':
        duvida.delete()
        messages.success(request, "Dúvida excluída com sucesso!")
        return redirect('lista_duvidas')
    return render(request, 'forum/exclui_duvida.html', {'duvida': duvida})

@login_required
def edita_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentário atualizado com sucesso!")
            return redirect('detalhes_duvida', id=comentario.duvida.id)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'forum/edita_comentario.html', {'form': form, 'duvida': comentario.duvida})

@login_required
def exclui_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user != comentario.autor and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para excluir este comentário.")
        return redirect('detalhes_duvida', id=comentario.duvida.id)
    if request.method == 'POST':
        comentario.delete()
        messages.success(request, "Comentário excluído com sucesso!")
        return redirect('detalhes_duvida', id=comentario.duvida.id)
    return render(request, 'forum/exclui_comentario.html', {'comentario': comentario})
