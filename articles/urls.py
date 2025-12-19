from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('articles/', views.articles_list, name='articles_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<int:article_id>/edit/', views.article_edit, name='article_edit'),

    # API endpoints
    path('api/articles/', views.api_articles, name='api_articles'),
    path('api/articles/<int:article_id>/', views.api_article_detail, name='api_article_detail'),
    path('api/articles/create/', views.api_article_create, name='api_article_create'),
    path('api/articles/<int:article_id>/update/', views.api_article_update, name='api_article_update'),
]