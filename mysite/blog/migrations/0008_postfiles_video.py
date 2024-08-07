# Generated by Django 5.0.7 on 2024-08-03 12:18

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_postfiles_audio_alter_postfiles_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='postfiles',
            name='video',
            field=models.FileField(blank=True, help_text='Put a video files only mp4', upload_to='files_of_posts/video', validators=[blog.models.validate_video_extension]),
        ),
    ]
