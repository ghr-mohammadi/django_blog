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
    # path('my-works/posts/<int:id>/', views.my_post, name='my_post'),
    # path('my-works/comments/<int:id>/', views.my_comment, name='my_comment'),
    path('search/', views.search, name='search'),
    path('logout/', views.logout_view, name='logout')
]
