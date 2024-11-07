from django.db import models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=45)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    datanasc = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=11)  

    def __str__(self):
        return self.nome

class Topico(models.Model):
    id_topico = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=45)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    disponivel_no_sistema = models.BooleanField(default=False)  
    def __str__(self):
        return self.nome

class Flashcard(models.Model):
    id_flashcard = models.AutoField(primary_key=True)
    texto_frente = models.TextField(max_length=60)
    texto_verso = models.TextField(max_length=60)
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.texto_frente


class FileUpload(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Quem fez o upload
    arquivo = models.FileField(upload_to='uploads/')  # O arquivo ou imagem
    legenda = models.CharField(max_length=255, blank=True)  # Legenda do arquivo
    data_upload = models.DateTimeField(auto_now_add=True)  # Data de upload

    def __str__(self):
        return f"{self.usuario.username} - {self.legenda}"

class Duvida(models.Model):
    titulo = models.CharField(max_length=255, default="Sem título")
    autor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    duvida = models.TextField()

    class Meta:
        verbose_name_plural = "Dúvidas"

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    duvida = models.ForeignKey(Duvida, related_name="comentarios", on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor} em {self.duvida}"

