# Generated by Django 5.1.1 on 2024-11-05 13:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topico',
            fields=[
                ('id_topico', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='uploads/')),
                ('legenda', models.CharField(blank=True, max_length=255)),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flashcard',
            fields=[
                ('id_flashcard', models.AutoField(primary_key=True, serialize=False)),
                ('texto_frente', models.TextField(max_length=60)),
                ('texto_verso', models.TextField(max_length=60)),
                ('usuario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('topico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.topico')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=45)),
                ('datanasc', models.DateField(blank=True, null=True)),
                ('cpf', models.CharField(max_length=11)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]