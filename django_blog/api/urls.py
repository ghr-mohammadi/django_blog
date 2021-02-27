from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('opinion/', views.opinion, name='opinion'),
    path('create-tag/', views.create_tag, name='create_tag')
]
