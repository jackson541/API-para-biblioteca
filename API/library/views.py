from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from library.models import Book
import json
    

def verifyCode(code):
    value = list(Book.objects.filter(code = code).values())

    if(value == []):
        return False

    return True



def bookList(request):
    books = list(Book.objects.all().values())
    return JsonResponse(books, safe = False)



def bookCreate(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        fields = ['code', 'title', 'author', 'date_launch', 'amount_available']

        for field in fields:
            try:
                body[field]
            except:
                return JsonResponse({"erro":'campo ' + field + ' não fornecido'}, safe=False)
        

        
        book = Book(
            code = body['code'],
            title = body['title'],
            author = body['author'],
            date_launch = body['date_launch'],
            date_register = body['date_register'] if 'date_register' in body else timezone.now(),
            amount_available = body['amount_available']
        )
    
        book.save()

    return JsonResponse({})



def bookEdit(request, code):
    if request.method == "PUT" and verifyCode(code):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        book = Book.objects.get(pk=code)

        for field in body:
            setattr(book, field, body[field])
            
        book.save()

    return JsonResponse({})



def bookDelete(request, code):
    if request.method == "DELETE" and verifyCode(code):
        book = Book.objects.get(code=code)
        book.delete()

    return JsonResponse({})


# Create your views here.
