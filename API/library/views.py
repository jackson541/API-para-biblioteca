from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from library.models import Book, Loan
import json
    

# Middlewares

def verifyCode(code):
    value = list(Book.objects.filter(code = code).values())

    if(value == []):
        return False

    return True


def verifyLoanId(id):
    value = list(Loan.objects.filter(pk = id).values())

    if(value == []):
        return False

    return True

# Book code

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
                return JsonResponse({"erro":'campo ' + field + ' nao fornecido'}, safe=False)
        

        
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


# Loan Code


def loanList (request):
    loans = list(Loan.objects.all().values())
    return JsonResponse(loans, safe = False)



def loanCreate (request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        fields = ['code_book', 'user', 'loan_date', 'devolution_date']

        
        for field in fields:
            try:
                body[field]
        
            except:
                return JsonResponse({
                    "error": "campo " + field + " nao foi informado"
                })

        book = Book.objects.get(pk = body['code_book'])

        loan = Loan(
            code_book = book,
            user = body['user'],
            loan_date = body['loan_date'] if 'loan_date' in body else timezone.now(),
            devolution_date = body['devolution_date']
        )

        loan.save()

    return JsonResponse({})



def loanEdit (request, id):
    if request.method == 'PUT' and verifyLoanId(id):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        loan = Loan.objects.get(pk=id)

        for field in body:
            setattr(loan, field, body[field])

        loan.save()

    return JsonResponse({})



def loanDelete (request, id):
    if request.method == "DELETE" and verifyLoanId(id):
        loan = Loan.objects.get(pk=id)
        loan.delete()
    
    return JsonResponse({})