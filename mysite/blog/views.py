from .models import Post, TextVideoClips
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm, AddPostForm, Files_for_post, TextClipsForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
import numpy as np
from moviepy.editor import *
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})

"""
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
"""


@require_POST
def add_post(request):
    post_form = AddPostForm(data=request.POST)
    file_form = Files_for_post(request.POST, request.FILES)
    if post_form.is_valid() and file_form.is_valid():
        post = post_form.save(commit=False)
        post.author = request.user
        post.save()
        file = file_form.save(commit=False)
        file.post = post
        file.save()
        return redirect('blog:user_post_list')


def user_post_list(request):
    post_list = Post.objects.filter(author=request.user)
    post_form = AddPostForm()
    file_form = Files_for_post()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/user_post_list.html', {'posts': posts, 'post_form': post_form, 'file_form': file_form})


def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})


def post_detail(request, id, post):
    post = get_object_or_404(Post,
                             slug=post,
                             id=id)

    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)

    # Список файлов поста
    files = post.files.all()

    # Форма для комментариев пользователей
    form = CommentForm()

    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'files': files,
                   'form': form,
                   'similar_posts': similar_posts})


def post_share(request, post_id):
    # Извлечь пост по его идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s ({cd['email']}) comments: {cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    post_url = post.get_absolute_url()

    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Назначить пользователя комментарию
        comment.user = request.user
        # Сохранить комментарий в базе данных
        comment.save()

    return redirect(post_url)


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


def text_clips(request):
    form = TextClipsForm()
    previously_clips = TextVideoClips.objects.all()
    if request.method == 'POST':
        clip_form = TextClipsForm(request.POST)
        if clip_form.is_valid():
            clip = clip_form.save(commit=False)
            clip.author = request.user
            clip.path_to_file = f"/media/generated_video/{clip.name_of_file}.mp4"
            clip.save()
            output_path = f'C:/Users/Mainuser/Desktop/Second_project/New_project/mysite/media/generated_video/{clip.name_of_file}.mp4'
            generate_video_with_text(clip.text, output_path)

            return redirect('blog:my_clips')

    return render(request, 'blog/post/my_clips.html', {'form': form, 'previously_clips': previously_clips})


def scroll_left(screenpos, i, nletters, total_duration):
    speed = 100
    total_width = 720
    letter_width = 80  # приблизительная ширина каждой буквы

    # Начальная позиция текста за пределами экрана
    start_position = np.array([total_width + i * letter_width, 150])
    return lambda t: start_position - np.array([speed * t, 0])

def moveLetters(letters, funcpos):
    return [letter.set_pos(funcpos(letter.screenpos, i, len(letters)))
            for i, letter in enumerate(letters)]

def generate_video_with_text(text, output_path):
    screensize = (720, 460)
    letter_clips = [TextClip(char, color='white', font="Arial-Bold", fontsize=150) for char in text]

    for i, letter in enumerate(letter_clips):
        letter.screenpos = np.array([i * 100, 0])

    total_width = len(text) * 100
    speed = 100
    total_duration = total_width / speed

    animated_clip = CompositeVideoClip(
        moveLetters(letter_clips, lambda screenpos, i, nletters: scroll_left(screenpos, i, nletters, total_duration)),
        size=screensize
    ).subclip(0, total_duration)

    animated_clip.write_videofile(output_path, fps=25, codec='libx264')