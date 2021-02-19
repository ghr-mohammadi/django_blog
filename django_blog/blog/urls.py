from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('category/<name>/', views.category, name='category'),
    path('tag/<name>/', views.tag, name='tag'),
    path('post/<int:id>/', views.post, name='post'),
    path('posts-of/<username>/', views.posts_of, name='posts_of'),
    path('search/', views.search, name='search'),
    path('logout/', views.logout_view, name='logout')
]
