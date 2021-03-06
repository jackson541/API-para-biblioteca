from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from library.models import Book, Loan
import json
    

# Middlewares

def verifyCode(code):
    return Book.objects.filter(code = code).exists()

def verifyLoanId(id):
    return Loan.objects.filter(pk = id).exists()



# Book code



def bookList(request):
    books = list(Book.objects.all().values())
    return JsonResponse(books, safe = False)



def bookView(request, code):
    if request.method == "GET" and verifyCode(code):
        book = list(Book.objects.filter(pk = code).values())
        return JsonResponse(book, safe=False)
    
    return JsonResponse({})



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
        
        if verifyCode(body['code']):
            return JsonResponse({
                "error": "código do livro já está cadastrado"
            })
        
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



def bookLoans(request, code):
    if request.method == "GET" and verifyCode(code):
        loans = list(Loan.objects.filter(code_book = code).values())
        return JsonResponse(loans, safe=False)

    return JsonResponse({})



# Loan Code


def loanList (request):
    loans = list(Loan.objects.all().values())
    return JsonResponse(loans, safe = False)



def loanView (request, id):
    if request.method == "GET" and verifyLoanId(id):
        loan = list(Loan.objects.filter(pk=id).values())

        return JsonResponse(loan, safe=False)

    return JsonResponse({})



def loanCreate (request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        fields = ['code_book', 'user', 'loan_date', 'devolution_date']

        #verificando se todos os campos foram passados
        for field in fields:
            try:
                body[field]
        
            except:
                return JsonResponse({
                    "error": "campo " + field + " nao foi informado"
                })

        if not(verifyCode(body['code_book'])):
            return JsonResponse({
                "error": "o livro com código " + body['code_book'] + " não está registrado no banco de dados"
            })


        counter = Loan.objects.filter(code_book = body['code_book']).count()
        book = Book.objects.get(pk = body['code_book'])

        if counter == book.amount_available:
            return JsonResponse({
                "error": "todos os livros com esse código já foram emprestados"
            })


       
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
        
        if 'code_book' in body:
            if not(verifyCode(body['code_book'])):
                return JsonResponse({
                    "error": "o código " + body['code_book'] + " não está registrado no banco de dados"
                })

            counter = Loan.objects.filter(code_book = body['code_book']).count()
            book = Book.objects.get(pk = body['code_book'])

            if counter == book.amount_available and loan.code_book != book:
                return JsonResponse({
                    "error": "todos os livros com esse código já foram emprestados"
                })

            #define o valor o livro e remove o campo do body para não dar conflito no for
            loan.code_book = book
            del body['code_book']

        #alterando todos os campos que foram passados no body
        for field in body:
            setattr(loan, field, body[field])

        loan.save()

    return JsonResponse({})



def loanDelete (request, id):
    if request.method == "DELETE" and verifyLoanId(id):
        loan = Loan.objects.get(pk=id)
        loan.delete()
    
    return JsonResponse({})



# searches



def searchBookTitle (request, title):
    if request.method == "GET":
        books = list(Book.objects.filter(title=title).values())

        return JsonResponse(books, safe=False)

    return JsonResponse({})



def searchBookAuthor (request, author):
    if request.method == "GET":
        books = list(Book.objects.filter(author=author).values())

        return JsonResponse(books, safe=False)

    return JsonResponse({})


#o date_launch deve ser passado no formato de data
#exemplo: 2019-01-01
def searchBookLaunch (request, date_launch):
    if request.method == "GET":
        try:
            #verifica se o formato da data passado é válido
            datetime.strptime(date_launch, "%Y-%m-%d")

            books = list(Book.objects.filter(date_launch=date_launch).values())

            return JsonResponse(books, safe=False)

        except:
            return JsonResponse({
                "error": "formato da data inválido. ex: 2000-10-01"
            })

    return JsonResponse({})



def searchBookUser (request, user):
    if request.method == "GET":
        books = []
        loans = Loan.objects.filter(user=user)

        for loan in loans:
            #transforma o objeto em um dicionário e remove a propriedade _state
            book = loan.code_book.__dict__
            del book['_state']

            books.append(book)
        
        return JsonResponse(books, safe=False)

    return JsonResponse({})
