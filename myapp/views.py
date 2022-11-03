# Import necessary classes
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

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
    # response = HttpResponse()
    # head = '<h1>' + 'This is an Online Store APP.' + '</h1>'
    # response.write(head)
    # return response
    return render(request, 'myapp/about.html')

def detail(request, cat_no) :
    lis=[]
    response = HttpResponse()
    prod_list = Product.objects.filter(category_id=cat_no)
    print(prod_list)
    cate = Category.objects.get(id=cat_no).name
    ware = Category.objects.get(id=cat_no).warehouse
    if (len(prod_list)==0):
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
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg':msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form':form, 'msg':msg,'prodlist':prodlist})

def productdetail(request, prod_id):

    if len(Product.objects.filter(id=prod_id)) == 0:
        msg = "Product not found"
        return render(request, 'myapp/productdetail.html', {'msg':msg})

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
    return render(request, 'myapp/productdetail.html', {'form':form, 'name':name, 'price':price, 'interested':interested})