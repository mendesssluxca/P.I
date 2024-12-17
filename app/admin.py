from django.contrib import admin

from django.contrib import admin
from .models import Usuario,  Topico, Flashcard


class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1

class TopicoAdmin(admin.ModelAdmin):
    list_display = ["id_topico", "nome"]
    search_fields = ["nome"]
    inlines = [FlashcardInline]


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["id_usuario", "nome", "cpf"]
    search_fields = ["nome", "cpf"]



admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Topico, TopicoAdmin)
admin.site.register(Flashcard)
