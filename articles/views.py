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