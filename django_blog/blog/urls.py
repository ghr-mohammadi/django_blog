from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('category/<name>/', views.category, name='category'),
    path('tag/<name>/', views.tag, name='tag'),
    path('logout/', views.logout_view, name='logout')
]
