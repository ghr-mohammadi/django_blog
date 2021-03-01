from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.categories, name='categories'),
    path('category/<name>/', views.category, name='category'),
    path('tag/', views.tags, name='tags'),
    path('tag/<name>/', views.tag, name='tag'),
    path('bests/', views.bests, name='bests'),
    path('post/<int:id>/', views.post, name='post'),
    path('posts-of/<username>/', views.posts_of, name='posts_of'),
    path('my-works/', views.my_works, name='my_works'),
    path('edit/', views.my_works),
    path('edit/posts/', views.my_works),
    path('edit/comments/', views.my_works),
    path('edit/posts/<int:id>/', views.edit_post, name='edit_post'),
    path('delete/posts/<int:id>/', views.delete_post, name='delete_post'),
    path('edit/comments/<int:id>/', views.edit_comment, name='edit_comment'),
    path('delete/comments/<int:id>/', views.delete_comment, name='delete_comment'),
    path('search/', views.search, name='search'),
    path('create-post/', views.create_post, name='create_post'),
    path('logout/', views.logout_view, name='logout')
]
