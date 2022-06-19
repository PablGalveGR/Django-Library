from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from api.serializers import BookSerializer
# Create your views here.
def index(request):
    """View function for home page of site."""
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_text_books =  Book.objects.filter(title__icontains='texto').count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.filter(name__icontains='fantasy').count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_text_books': num_text_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'num_visits' : num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

## Class based View
from django.views import generic

class BookListView(generic.ListView):
  model = Book
  ##paginate_by = 10
  def get_queryset(self):
    return Book.objects.all()
  def get_context_data(self, **kwargs):
    context = super(BookListView, self).get_context_data(**kwargs)
    context['cosas'] = 'Cosas'
    return context



#########Server side pagination############
    
## Class based view
class BookDetailView(generic.DetailView):
  model = Book
## Class Based Author view
class AuthorListView(generic.ListView):
  model = Author
  paginate_by = 10
  def get_queryset(self):
    return Author.objects.all()
  def get_constext_data(self, **kwargs):
    context = super(AuthorListView, self).get_context_data(**kwargs)
    context['cosas'] = 'Cosas'
    return context

class AuthorDetailView(generic.DetailView):
  model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
class LoanedBooksAllListView(LoginRequiredMixin, generic.ListView):
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_all.html'
  paginate_by = 10
  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o').order_by('borrower')

## Forms Methods
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

## Author Model forms for generic view Edition
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

## Book Model forms for generic view Edition
from catalog.models import Book

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
