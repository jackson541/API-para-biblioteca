from django.urls import path,include
from library import views

urlpatterns = [
    
    path('books/', include([
        path('', views.bookList),
        path('create', views.bookCreate),
        path('edit/<str:code>', views.bookEdit),
        path('delete/<str:code>', views.bookDelete),
        path('<str:code>', views.bookView),
        path('loans/<str:code>', views.bookLoans)
    ])),

    path('loans/', include([
        path('', views.loanList),
        path('create', views.loanCreate),
        path('edit/<int:id>', views.loanEdit),
        path('delete/<int:id>', views.loanDelete)
    ]))
]