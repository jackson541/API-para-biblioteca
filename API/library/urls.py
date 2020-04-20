from django.urls import path,include
from library import views

urlpatterns = [
    
    path('books/', include([
        path('', views.bookList),
        path('create', views.bookCreate),
        path('edit/<str:code>', views.bookEdit),
        path('delete/<str:code>', views.bookDelete),
        path('loans/<str:code>', views.bookLoans),
        path('<str:code>', views.bookView)
    ])),

    path('loans/', include([
        path('', views.loanList),
        path('create', views.loanCreate),
        path('edit/<int:id>', views.loanEdit),
        path('delete/<int:id>', views.loanDelete),
        path('<str:id>', views.loanView)
    ])),

    path('search/book/', include([
        path('title/<str:title>', views.searchBookTitle),
        path('author/<str:author>', views.searchBookAuthor),
        path('launch/<str:date_launch>', views.searchBookLaunch),
        path('user/<str:user>', views.searchBookUser)
    ]))
]