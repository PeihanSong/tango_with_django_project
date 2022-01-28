from django.shortcuts import render
from django.http import  HttpResponse

# Create your views here.


def index(request):
    context_dictionary = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/index.html', context=context_dictionary)


def about(request):
    context_dictionary = {'yourname': 'Peihan Song'}
    return render(request, 'rango/about.html', context=context_dictionary)
