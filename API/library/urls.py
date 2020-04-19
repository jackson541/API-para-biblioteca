from django.urls import path,include
from library import views

urlpatterns = [
    
    path('books/', include([
        path('', views.bookList),
        path('<str:code>', views.bookView),
        path('create', views.bookCreate),
        path('edit/<str:code>', views.bookEdit),
        path('delete/<str:code>', views.bookDelete),
        path('loans/<str:code>', views.bookLoans)
    ])),

    path('loans/', include([
        path('', views.loanList),
        path('<str:id>', views.loanView),
        path('create', views.loanCreate),
        path('edit/<int:id>', views.loanEdit),
        path('delete/<int:id>', views.loanDelete)
    ]))
]