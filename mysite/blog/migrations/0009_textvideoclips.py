# Generated by Django 5.0.7 on 2024-08-07 20:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_postfiles_video'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TextVideoClips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_file', models.CharField(max_length=100, verbose_name='Введите желаемое название файла')),
                ('text', models.CharField(max_length=100, verbose_name='Введите текст')),
                ('path_to_file', models.CharField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clips', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
