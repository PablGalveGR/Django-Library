from http import server
from django.contrib.auth.models import User, Group
from catalog.models import Author, Book, BookInstance
from catalog.models import Genre
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import views, status
from django_filters  import rest_framework as filters
from django.db.models import Q
import math
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from api.serializers import UserSerializer, GroupSerializer, BookSerializer, GenreSerializer, AuthorSerializer, BookInstanceSerializer
##Filters 
class BookFilterSet(filters.FilterSet):
    class Meta:
        model =  Book
        fields = {
            'author__id': ['exact'],
            'id':['exact'],
            'title':['icontains']
        }
class AuthorFilterSet(filters.FilterSet):
    class Meta:
        model = Author
        fields = {
            'first_name': ['contains'],
            'last_name': ['contains'],
            'id':['exact']
        }
class BookInstanceFilterSet(filters.FilterSet):
    class Meta:
        model =  BookInstance
        fields = {
            'id': ['exact'],
            'status': ['contains'],
            'borrower': ['exact']
        }
##Views
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class BooksViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows Books to be viewed or edited.
  """
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  filterset_class = BookFilterSet
  
  def list(request, *args, **kargs):
    ##print("Request???:"+str(args))
    request = args[0]
    ##print("Request: "+ str(request))
    books = Book.objects.all()
    total = books.count()
    search = request.GET.get('search[value]')
    column = request.GET.get('order[0][column]')
    order = request.GET.get('order[0][dir]')
    def getColumnNameAndOrder(num, order):
      columns = {
          '0':'title',
          '1':'author',
          '2':'summary',
          '3':'isbn',
          '4':'genre' 
      }
      column = columns[num]
      if order == 'desc':
          column = '-'+column
      return column
    if request.GET.get("id"):
      id = request.GET.get("id")
      books = books.filter(Q(pk__exact=id))
      data = [book.to_dict_json() for book in books]
      return Response(data, status=status.HTTP_200_OK, template_name=None, content_type=None) 
    else:
      if search and search != "" and not request.GET.get('author__id'):
          books = books.filter(
            Q(title__icontains=search)|
            Q(author__first_name__icontains=search)|
            Q(author__last_name__icontains=search) |
            Q(summary__icontains=search) |
            Q(isbn__icontains=search) |
            Q(genre__name__icontains=search)
          )
      elif request.GET.get('author__id'):
        author_id = request.GET.get('author__id')
        books = books.filter(
            Q(author__pk__icontains=author_id)&(
              Q(title__icontains=search)|
              Q(summary__icontains=search) |
              Q(isbn__icontains=search) |
              Q(genre__name__icontains=search)
            )
            
          )

      total_Filtered = books.count()   
      ####Order by
      if(column):
          print('Order: ' + getColumnNameAndOrder(column, order))
          books = books.order_by(getColumnNameAndOrder(column, order))
      _start = request.GET.get('start')
      _length = request.GET.get('length')
      print("Start: " + str(_length))
      if _start and _length:
          start = int(_start)
          length = int(_length)
          page = math.ceil(start / length) + 1  # [opcional]
          per_page = length  # [opcional]
          books = books[start:start + length]
      
      data = [book.to_dict_json() for book in books]
      data2 = BookSerializer(books, many = True)
      
      print("Number Of books before filter: "+str(total))
      print("Number Of books after filter: "+str(total_Filtered) )
      data3 = [book.to_dict_json() for book in books]
      ##print("Data Serializer: " + str(data3))
      response = {
          'data': data3,
          'recordsTotal': total,
          'recordsFiltered': total,
          'page': page,
          'per_page': per_page,
          'length':per_page,
          'start' : start
          }
      if total_Filtered != total:
          response['recordsFiltered'] = total_Filtered
      print("Data Respose: " + str(response))
      return Response(response, status=status.HTTP_200_OK, template_name=None, content_type=None)
    

class BooksInstanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Books to be viewed or edited.
    """
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    filterset_class = BookInstanceFilterSet
    def list(request, *args, **kargs):
      ##print("Request???:"+str(args))
      request = args[0]
      ##print("Request: "+ str(request))
      instances = BookInstance.objects.all()
      total = instances.count()
      search = request.GET.get('search[value]')
      column = request.GET.get('order[0][column]')
      order = request.GET.get('order[0][dir]')
      def getColumnNameAndOrder(num, order, pageType):
        columns = {}
        if pageType == "All":
          columns = {
              '0':'book',
              '1':'due_back',
              '2':'status',
              '3':'borrower'
          }
        elif pageType == "Detail":
          columns = {
              '0':'status',
              '1':'due_back',
              '2':'imprint',
              '3':'id'
          }
        elif pageType =="User":
          columns = {
              '0':'book',
              '1':'due_back'
          }    
        column = columns[num]
        if order == 'desc':
            column = '-'+column
        return column
      ##Show only instances from one book if the id is passed
      if request.GET.get("id"):
        id = request.GET.get("id")
        instances = instances.filter(status__exact='o')
        instances = instances.filter(Q(book_pk__exact=id))
        data = [instance.to_dict_json() for instance in instances]
        return Response(data, status=status.HTTP_200_OK, template_name=None, content_type=None) 
      else:
        instances = instances.filter(status__exact='o')
        if search and search != "" and not request.GET.get('borrower__id') and not request.GET.get('book'):
          instances = instances.filter(
            Q(book__title__icontains=search)|
            Q(due_back__icontains=search)|
            Q(borrower__username__icontains=search)
            )
            ####Order by
          if(column):
            print('Order: ' + getColumnNameAndOrder(column, order,"All"))
            instances = instances.order_by(getColumnNameAndOrder(column, order,"All"))
        elif request.GET.get('borrower'):
          instances = instances.filter(status__exact='o')
          borrower_id = request.GET.get('borrower')
          instances = instances.filter(
            Q(borrower__pk__exact=borrower_id)&(
            Q(book__title__icontains=search)|
            Q(due_back__icontains=search)
            )
            )
            ####Order by
          if(column):
            print('Order: ' + getColumnNameAndOrder(column, order,"User"))
            instances = instances.order_by(getColumnNameAndOrder(column, order,"User"))
        elif request.GET.get('book'):
          bookId = request.GET.get('book')
          instances = BookInstance.objects.all()
          instances = instances.filter(
            Q(book__pk__exact=bookId)&(
            Q(status__icontains=search)|
            Q(due_back__icontains=search)|
            Q(imprint__icontains=search)|
            Q(id__icontains=search)
            )
            )
            ####Order by
          if(column):
            print('Order: ' + getColumnNameAndOrder(column, order,"Detail"))
            instances = instances.order_by(getColumnNameAndOrder(column, order,"Detail"))
        total_Filtered = instances.count()   
        _start = request.GET.get('start')
        _length = request.GET.get('length')
        print("Start: " + str(_length))
        if _start and _length:
            start = int(_start)
            length = int(_length)
            page = math.ceil(start / length) + 1  # [opcional]
            per_page = length  # [opcional]
            instances = instances[start:start + length]
        
        data = [instance.to_dict_json() for instance in instances]
        print("Number Of books before filter: "+str(total))
        print("Number Of books after filter: "+str(total_Filtered) )
        ##print("Data Serializer: " + str(data3))
        response = {
            'data': data,
            'recordsTotal': total,
            'recordsFiltered': total,
            'page': page,
            'per_page': per_page,
            'length':per_page,
            'start' : start
            }
        if total_Filtered != total:
            response['recordsFiltered'] = total_Filtered
        #print("Data Respose: " + str(response))
        return Response(response, status=status.HTTP_200_OK, template_name=None, content_type=None)

    
    
class AuthorsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Authors to be viewed or edited.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_class = AuthorFilterSet
    def list(request, *args, **kargs):
        ##print("Request???:"+str(args))
        request = args[0]
        ##print("Request: "+ str(request))
        authors = Author.objects.all()
        total = authors.count()
        search = request.GET.get('search[value]')
        column = request.GET.get('order[0][column]')
        order = request.GET.get('order[0][dir]')
        def getColumnNameAndOrder(num, order):
          columns = {
              '0':'first_name',
              '1':'last_name',
              '2':'date_of_birth',
              '3':'date_of_death',
          }
          column = columns[num]
          if order == 'desc':
              column = '-'+column
          return column
        if request.GET.get('id'):
          id = request.GET.get('id')
          authors = authors.filter(Q(pk__exact=id))
          data = [author.to_dict_json() for author in authors] 
          return Response(data, status=status.HTTP_200_OK, template_name=None, content_type=None) 
              
        else:
          if search and search != "":
              authors = authors.filter(
              Q(first_name__icontains=search)|
              Q(last_name__icontains=search)|
              Q(date_of_birth__icontains=search) |
              Q(date_of_death__icontains=search)
              )

          total_Filtered = authors.count()   
          ####Order by
          if(column):
              print('Order: ' + getColumnNameAndOrder(column, order))
              authors = authors.order_by(getColumnNameAndOrder(column, order))
          _start = request.GET.get('start')
          _length = request.GET.get('length')
          print("Start: " + str(_length))
          if _start and _length:
              start = int(_start)
              length = int(_length)
              page = math.ceil(start / length) + 1  # [opcional]
              per_page = length  # [opcional]
              authors = authors[start:start + length]
          
          data = [author.to_dict_json() for author in authors]        
          print("Number Of books before filter: "+str(total))
          print("Number Of books after filter: "+str(total_Filtered) )
          ##print("Data Serializer: " + str(data3))
          response = {
              'data': data,
              'recordsTotal': total,
              'recordsFiltered': total,
              'page': page,
              'per_page': per_page,
              'length':per_page,
              'start' : start
              }
          if total_Filtered != total:
              response['recordsFiltered'] = total_Filtered
          print("Data Respose: " + str(response))
          return Response(response, status=status.HTTP_200_OK, template_name=None, content_type=None)
    
class GenresViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Genres to be viewed or edited.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

