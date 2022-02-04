from django.shortcuts import render

from rango.models import Category, Page


# Create your views here.


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]

    context_dictionary = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!', 'categories': category_list}
    most_viewed_pages = Page.objects.order_by('-views')[:5]
    context_dictionary['pages'] = most_viewed_pages
    return render(request, 'rango/index.html', context=context_dictionary)


def about(request):
    context_dictionary = {'yourname': 'Peihan Song'}
    return render(request, 'rango/about.html', context=context_dictionary)


def show_category(request, category_name_slug):
    context_dictionary = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dictionary['pages'] = pages

        context_dictionary['category'] = category
    except Category.DoesNotExist:
        context_dictionary['category'] = None
        context_dictionary['pages'] = None

    return render(request, 'rango/category.html', context=context_dictionary)
