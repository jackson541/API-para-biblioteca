from django.shortcuts import render
from django.http import JsonResponse
from library.models import Book
import json


def bookList(request):
    books = list(Book.objects.all().values())
    return JsonResponse(books, safe = False)



def bookCreate(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        book = Book(
            code = body['code'],
            title = body['title'],
            author = body['author'],
            date_launch = body['date_launch'],
            date_register = body['date_register'],
            amount_available = body['amount_available']
        )
    
        book.save()

    return JsonResponse({})



def bookEdit(request, code):
    if request.method == "PUT":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        book = Book.objects.get(pk=code)

        book.code = body['code'] if 'code' in body else book.code
        book.title = body['title'] if 'title' in body else book.title
        book.author = body['author'] if 'author' in body else book.author
        book.date_launch = body['date_launch'] if 'date_launch' in body else book.date_launch
        book.date_register = body['date_register'] if 'date_register' in body else book.date_register
        book.amount_available = body['amount_available'] if 'amount_available' in body else book.amount_available
    
        book.save()

    return JsonResponse({})



def bookDelete(request, code):
    if request.method == "DELETE":
        book = Book.objects.get(code=code)
        book.delete()
    
    return JsonResponse({})


# Create your views here.
