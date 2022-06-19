import string
import random
from django.core.management.base import BaseCommand, CommandError
from catalog.models import Book, Author, Genre
from catalog.views import BookCreate
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)
class Command(BaseCommand):
  help = "Creates any given number of books"
  def add_arguments(self, parser):
      parser.add_argument('total', type=int, help='Indicates the number of users to be created')

  def handle(self, *args, **kwargs):
    total = kwargs['total']
    randString = ""
    authors = Author.objects.all()
    genres = Genre.objects.all()
    while total >0:
      ####Commands here###
      ##BookCreate.fields = ['title', 'author', 'summary', 'isbn', 'genre']
      randString = get_random_string(6)
      randNum = random.randint(0,1)
      authorSelected = Author.objects.filter(pk = authors[randNum].pk) 
      genreSelected = Genre.objects.filter(pk = genres[randNum].pk)
      book = Book(title = randString, author = authorSelected[0], summary = randString, 
      isbn = random_with_N_digits(13))
      book.save()
      book.genre.set(genreSelected)
      ###Commands end####
      print("Book tittle: " + randString + "||Book ID: "+str(book.pk))
      total -=1
  
  
    