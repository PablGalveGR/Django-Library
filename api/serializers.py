from pyexpat import model
from django.contrib.auth.models import User, Group
from catalog.models import Author, BookInstance, Genre
from rest_framework import serializers
from catalog.models import Book


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
##My serializers
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']
class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    genre_name = serializers.StringRelatedField(many=True, source = "genre")
    class Meta:
      model = Book
      fields = ['title', 'author_name', 'isbn', 'summary', 'genre_name', 'author_id', 'id']

##Author serializer
class AuthorSerializer(serializers.ModelSerializer):
  date_of_birth = serializers.DateField()
  date_of_birth = serializers.DateField()
  class Meta:
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'id']

class BookInstanceSerializer(serializers.ModelSerializer):
    due_back = serializers.DateField()
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_id = serializers.CharField(source='book.id', read_only=True)
    borrower_user = serializers.StringRelatedField(source='borrower.username', read_only=True)
    ##Check this to get the status string like "On loan, Available"
    ##status_string = serializers.StringRelatedField(source='status.get_status_display', read_only=True)
    class Meta:
      model = BookInstance
      fields = ['book_title', 'due_back', 'status', 'book_id', 'borrower', 'borrower_user', 'id', 'imprint']




