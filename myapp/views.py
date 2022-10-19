# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import render
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of categories: ' + '</p>'
    response.write(heading1)
    for category in cat_list:
        para = '<p>'+ str(category.id) + ': ' + str(category) + '</p>'
        response.write(para)

    prod_list = Product.objects.all().order_by('-price')[:20]
    heading2 = '<p>' + 'List of products: ' + '</p>'
    response.write(heading2)
    for prod in prod_list:
        para1 = '<p>' + str(prod.name) + ': $' + str(prod.price) + '</p>'
        response.write(para1)

    return response


def about(request):
    response = HttpResponse()
    head = '<h1>' + 'This is an Online Store APP.' + '</h1>'
    response.write(head)
    return response

def detail(request, cat_no) :
    response = HttpResponse()
    prod_list = Product.objects.filter(category_id=cat_no)
    if (len(prod_list)==0):
        get_object_or_404(Product.objects.filter(category_id=cat_no))
    heading2 = '<p>' + 'List of products: ' + '</p>'
    response.write(heading2)
    for prod in prod_list:
        prodl = '<p>' + str(prod.name) + ': $' + str(prod.price) + '</p>'
        response.write(prodl)
    return response
