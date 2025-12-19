from django.shortcuts import render, redirect, get_object_or_404
from .models import Article


def articles_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'articles/list.html', {'articles': articles})


def article_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author', 'Аноним')

        if title and content:
            Article.objects.create(
                title=title,
                content=content,
                author=author
            )
            return redirect('articles_list')

    return render(request, 'articles/create.html')


def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.author = request.POST.get('author', article.author)
        article.save()
        return redirect('articles_list')

    return render(request, 'articles/edit.html', {'article': article})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# API: Получить все статьи
def api_articles(request):
    articles = Article.objects.all().order_by('-created_at')
    articles_data = [
        {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author': article.author,
            'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for article in articles
    ]
    return JsonResponse(articles_data, safe=False)


# API: Получить конкретную статью
def api_article_detail(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        article_data = {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author': article.author,
            'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return JsonResponse(article_data)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Статья не найдена'}, status=404)


# API: Создать статью (без CSRF для тестирования)
@csrf_exempt
def api_article_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Проверяем обязательные поля
            if 'title' not in data or 'content' not in data:
                return JsonResponse({'error': 'Требуются поля title и content'}, status=400)

            # Создаем статью
            article = Article.objects.create(
                title=data['title'],
                content=data['content'],
                author=data.get('author', 'Аноним')
            )

            return JsonResponse({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'author': article.author,
                'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'message': 'Статья успешно создана'
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный JSON формат'}, status=400)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


# API: Обновить статью
@csrf_exempt
def api_article_update(request, article_id):
    if request.method == 'PUT':
        try:
            article = Article.objects.get(id=article_id)
            data = json.loads(request.body)

            if 'title' in data:
                article.title = data['title']
            if 'content' in data:
                article.content = data['content']
            if 'author' in data:
                article.author = data['author']

            article.save()

            return JsonResponse({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'author': article.author,
                'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'message': 'Статья успешно обновлена'
            })
        except Article.DoesNotExist:
            return JsonResponse({'error': 'Статья не найдена'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный JSON формат'}, status=400)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)