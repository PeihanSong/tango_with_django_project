from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
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


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dictionary = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dictionary)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))

            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html')


def some_view(request):
    if request.user.is_authenticated():
        return HttpResponse("You are logged in.")

    else:
        return HttpResponse("You are not logged in")


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
