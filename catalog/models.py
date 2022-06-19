import string
from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
 ####Server side datatables
from django.db.models import Q

# Create your models here.

#Genre model
class Genre(models.Model):
  name = models.CharField(max_length=200, help_text='Enter a book genre(e.g. Science Fiction)')
  def __str__(self):
    return self.name
#Book model
class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
  summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
  isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
#Many to many genre-books
  genre = models.ManyToManyField(Genre, help_text = 'Select a genre for this book')
  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('book-detail', args=[str(self.id)])

  def display_genre(self):
    """Create a string for the Genre. This is required to display genre in Admin."""
    return ', '.join(genre.name for genre in self.genre.all()[:3])

  def countInstaces(book):
    count = 0
    for instance in book.bookinstance_set.all:
      count +=1
    return count

  display_genre.short_description = 'Genre'
  ####Server side datatables
  def to_dict_json(self):
    genre = self.display_genre()
    data = {
      'title' : self.title,
      'author_name' : self.author.first_name+", "+ self.author.last_name,
      'isbn' : self.isbn,
      'summary' : self.summary,
      'genre_name' : genre,
      'author_id' : self.author.pk,
      'id': self.pk
    }
    return data
  
#Book instance model
class BookInstance(models.Model):
  id = models.UUIDField(primary_key = True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
  book = models.ForeignKey('Book', on_delete = models.RESTRICT, null=True)
  imprint = models.CharField(max_length=200)
  due_back = models.DateField(null=True, blank=True)
  borrower = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank = True)
  LOAN_STATUS=(
    ('m', 'maintenance'),
    ('o','On loan'),
    ('a','Available'),
    ('r','Reserved'),
  )
  status = models.CharField(
    max_length=1,
    choices=LOAN_STATUS,
    blank=True,
    default='m',
    help_text='Book availability',
    )
  class Meta:
    ordering = ['due_back']
    permissions = (("can_mark_returned", "Set book as returned"),)

  def __str__(self):
    """String for representing the Model object."""
    return f'{self.id} ({self.book.title})'
    ####Server side datatables
  def to_dict_json(self):
    data = {
      'book_title': self.book.title,
      'due_back' : self.due_back, 
      'status' : self.status,
      'book_id' : self.book.pk,
      'borrower' : str(self.borrower), 
      'borrower_user': str(self.borrower),
      'id' : self.pk, 
      'imprint': self.imprint
    }
    return data
  @property
  def is_over_due(self):
    if self.due_back and date.today() > self.due_back:
      return True
    return False

##Autor model
class Author(models.Model):
  """Model representing an author."""
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  date_of_birth = models.DateField(null=True, blank=True)
  date_of_death = models.DateField('Died', null=True, blank=True)

  class Meta:
    ordering = ['last_name', 'first_name']

  def get_absolute_url(self):
    """Returns the url to access a particular author instance."""
    return reverse('author-detail', args=[str(self.id)])

  def __str__(self):
    """String for representing the Model object."""
    return f'{self.first_name}, {self.last_name}'
  def get_full_name(self):
    return self.first_name +", " + self.last_name
####Server side datatables
  def to_dict_json(self):
    data = {
      'first_name' : self.first_name,
      'last_name' : self.last_name, 
      'date_of_birth' : self.date_of_birth,
      'date_of_death' : self.date_of_death,
      'id' : self.pk
    }
    return data