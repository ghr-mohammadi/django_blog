from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('category/<name>/', views.category, name='category'),
    path('tag/<name>/', views.tag, name='tag'),
    path('post/<int:id>/', views.post, name='post'),
    path('posts-of/<int:id>/', views.posts_of, name='posts_of'),
    path('logout/', views.logout_view, name='logout')
]
