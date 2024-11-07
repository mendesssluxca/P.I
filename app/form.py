from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Usuario, Flashcard, Topico, FileUpload, Duvida, Comentario


class DuvidaForm(forms.ModelForm):
    class Meta:
        model = Duvida
        fields = ['titulo', 'duvida']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        
class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['texto_frente', 'texto_verso', 'topico']  

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

class CustomUserCreationForm(UserCreationForm):
    nome = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    cpf = forms.CharField(max_length=11, required=True)  
    datanasc = forms.DateField(required=True)  

    class Meta:
        model = User
        fields = ("nome","email","cpf","datanasc", "username", "password1", "password2" )

    def save(self, commit=True):
        user = super().save(commit)
        usuario = Usuario(
            user=user,
            nome=self.cleaned_data['nome'],
            datanasc=self.cleaned_data['datanasc'],
            cpf=self.cleaned_data['cpf']
        )
        if commit:
            usuario.save()
        return user
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'datanasc', 'cpf']
        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'datanasc', 'cpf'] 


class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = ['nome']  

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['arquivo', 'legenda']