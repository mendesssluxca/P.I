from django.db import migrations

def adicionar_topicos(apps, schema_editor):
    Topico = apps.get_model('app', 'Topico')  # Substitua 'nome_do_app' pelo nome do seu app

    # Lista de tópicos de Fisiologia Humana
    topicos = [
        "Sistema Cardiovascular",
        "Sistema Respiratório",
        "Sistema Nervoso Central",
        "Sistema Nervoso Periférico",
        "Sistema Digestório",
        "Sistema Endócrino",
        "Sistema Imunológico",
        "Sistema Renal",
        "Sistema Reprodutor",
        "Fisiologia Muscular",
    ]

    for nome_topico in topicos:
        Topico.objects.create(nome=nome_topico, disponivel_no_sistema=True)

def remover_topicos(apps, schema_editor):
    Topico = apps.get_model('app', 'Topico')
    topicos = [
        "Sistema Cardiovascular",
        "Sistema Respiratório",
        "Sistema Nervoso Central",
        "Sistema Nervoso Periférico",
        "Sistema Digestório",
        "Sistema Endócrino",
        "Sistema Imunológico",
        "Sistema Renal",
        "Sistema Reprodutor",
        "Fisiologia Muscular",
    ]

    Topico.objects.filter(nome__in=topicos).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),  # Coloque a dependência correta aqui
    ]

    operations = [
        migrations.RunPython(adicionar_topicos, remover_topicos),
    ]
