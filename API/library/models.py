from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Book (models.Model):
    code = models.CharField(max_length = 100, primary_key = True)
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 100)
    date_launch = models.DateField()
    #alterar para django.utils.timezone.now()
    date_register = models.DateField(default = timezone.now())
    amount_available = models.IntegerField()

class Loan (models.Model):
    code_book = models.ForeignKey('Book', on_delete = models.CASCADE)
    user = models.CharField(max_length = 100)
    loan_date = models.DateField(default = timezone.now())
    devolution_date = models.DateField()