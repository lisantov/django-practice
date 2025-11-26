from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book, Author, BookInstance, Genre, Language

def index(request):
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_languages = Language.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_war = Book.objects.filter(title__icontains='Война').count()

    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_languages': num_languages,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_war': num_war,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    paginate_by = 3

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'
    paginate_by = 3

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = 'bookinstance_list'
    template_name = 'catalog/book_list_borrowed_user.html'
    paginate_by = 3

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    context_object_name = 'bookinstance_list'
    template_name = 'catalog/book_list_borrowed.html'
    paginate_by = 3

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )