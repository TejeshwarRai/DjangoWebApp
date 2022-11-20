# Import necessary classes
import random
import string

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import *
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404


# Create your views here.

# def index(request):
#     cat_list = Category.objects.all().order_by('id')[:10]
#     response = HttpResponse()
#     heading1 = '<p>' + 'List of categories: ' + '</p>'
#     response.write(heading1)
#     for category in cat_list:
#         para = '<p>'+ str(category.id) + ': ' + str(category) + '</p>'
#         response.write(para)
#
#     prod_list = Product.objects.all().order_by('-price')[:20]
#     heading2 = '<p>' + 'List of products: ' + '</p>'
#     response.write(heading2)
#     for prod in prod_list:
#         para1 = '<p>' + str(prod.name) + ': $' + str(prod.price) + '</p>'
#         response.write(para1)
#
#     return response

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'cat_list': cat_list})


def about(request):
    if 'about_visits' in request.COOKIES.keys():
        number_visits = request.COOKIES['about_visits']
        number_visits = int(number_visits) + 1
    else:
        number_visits = 1

    response = render(request, 'myapp/about.html', {'number_visits': number_visits})
    response.set_cookie('about_visits', value=number_visits, max_age=300)
    # response = HttpResponse()
    # head = '<h1>' + 'This is an Online Store APP.' + '</h1>'
    # response.write(head)
    return response
    # return render(request, 'myapp/about.html')


def detail(request, cat_no):
    lis = []
    response = HttpResponse()
    prod_list = Product.objects.filter(category_id=cat_no)
    # print(prod_list)
    cate = Category.objects.get(id=cat_no).name
    ware = Category.objects.get(id=cat_no).warehouse
    if (len(prod_list) == 0):
        get_object_or_404(Product.objects.filter(category_id=cat_no))
    heading2 = '<p>' + 'List of products: ' + '</p>'
    response.write(heading2)
    for prod in prod_list:
        prodl = '<p>' + str(prod.name) + ': $' + str(prod.price) + '</p>'
        lis.append(str(prod.name))
        response.write(prodl)
    # return response
    return render(request, 'myapp/detail.html', {'prod_list': prod_list, 'cate': cate, 'ware': ware})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.product.stock -= order.num_units
                order.product.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    if len(Product.objects.filter(id=prod_id)) == 0:
        msg = "Product not found"
        return render(request, 'myapp/productdetail.html', {'msg': msg})

    name = Product.objects.get(id=prod_id).name
    price = Product.objects.get(id=prod_id).price
    interested = Product.objects.get(id=prod_id).interested

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if request.POST.get('interested') == '1':
                Product.objects.filter(id=prod_id).update(interested=F('interested') + 1)
        return redirect('myapp:index')
    else:
        form = InterestForm()
    return render(request, 'myapp/productdetail.html',
                  {'form': form, 'name': name, 'price': price, 'interested': interested})


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test  # Create your views here.


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if 'last_login' in request.session:
                    messages.success(request, 'Last login date and time: ' + str(request.session['last_login']))
                else:
                    request.session['last_login'] = str(timezone.now())
                    # print(request.session['last_login'])
                    messages.success(request, "Your last login was more than 1 hour ago")

                request.session['last_login'] = str(timezone.now())
                request.session['username'] = username
                request.session['user_first_name'] = user.first_name
                request.session['user_last_name'] = user.last_name
                request.session.set_expiry(3600)

                # return HttpResponseRedirect(reverse('myapp:index'))
                return HttpResponseRedirect(reverse('myapp:myorders'))

                # return redirect(request.GET.get('next', 'myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            userForm = form.save(commit=False)
            userForm.password = make_password(form.cleaned_data['password'])
            userForm.save()
            form.save_m2m()
            # g = Group.objects.get(name='Client')
            # g.user_set.add(userForm)
            print(userForm)
            return HttpResponseRedirect(reverse('myapp:index'))
        else:
            return HttpResponse('Error during registration')
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'form': form})



@login_required(login_url='myapp:login')
def myorders(request):
    client_list = Client.objects.all().order_by('id')
    client_list = [i.username for i in client_list]

    if f'{request.user}' in client_list:
        order_list = Order.objects.filter(client__username=request.user)
        return render(request, 'myapp/myorders.html', {"order_list": order_list})
    else:
        return HttpResponse('You are not a registered client!')

