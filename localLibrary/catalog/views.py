from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language


def index(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_languages = Language.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_war = Book.objects.filter(title__contains='Война').count()

    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_languages': num_languages,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_war': num_war,
    }

    return render(request, 'catalog/index.html', context=context)