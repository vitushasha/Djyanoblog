from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError


def validate_audio_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.wav', '.flac', '.aac']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def validate_video_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    objects = models.Manager()
    published = PublishedManager()

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.id,
                             self.slug])

    def __str__(self):
        return self.title


class PostFiles(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='files')

    image = models.ImageField(upload_to="files_of_posts/images", help_text='Put an image', blank=True)
    audio = models.FileField(upload_to="files_of_posts/audio", validators=[validate_audio_extension], help_text='Put an audio', blank=True)
    video = models.FileField(upload_to='files_of_posts/video', validators=[validate_video_extension], help_text='Put a video files only mp4', blank=True)

    def __str__(self):
        return 'files'


class TextVideoClips(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clips', default=1)
    name_of_file = models.CharField(max_length=100, verbose_name='Введите желаемое название файла, только латиница, без пробелов')
    text = models.CharField(max_length=100, verbose_name='Введите текст')
    path_to_file = models.CharField()



class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User,
                             on_delete=models.DO_NOTHING,
                             default=None)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.user.first_name} on {self.post}'