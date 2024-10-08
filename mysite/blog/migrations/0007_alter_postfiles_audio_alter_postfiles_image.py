# Generated by Django 5.0.7 on 2024-07-27 07:28

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_slug_postfiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfiles',
            name='audio',
            field=models.FileField(blank=True, help_text='Put an audio', upload_to='files_of_posts/audio', validators=[blog.models.validate_audio_extension]),
        ),
        migrations.AlterField(
            model_name='postfiles',
            name='image',
            field=models.ImageField(blank=True, help_text='Put an image', upload_to='files_of_posts/images'),
        ),
    ]
