from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # представления поста
    path('', views.post_list, name='post_list'),

    path('my_posts', views.user_post_list, name='user_post_list'),

    path('my_posts/add_posts', views.add_post, name='add_post'),

    path('my_clips/', views.text_clips, name='my_clips'),

    # path('', views.PostListView.as_view(), name='post_list'),

    path('<int:id>/<slug:post>/',
         views.post_detail,
         name='post_detail'),

    path('<int:post_id>/share/',
         views.post_share, name='post_share'),

    path('tag/<slug:tag_slug>/',
         views.post_list, name='post_list_by_tag'),

    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),

    path('search/', views.post_search, name='post_search'),
]