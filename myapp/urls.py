from django.urls import path, re_path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path('<int:cat_no>/', views.detail, name="detail"),
    path(r'products/', views.products, name="products"),
    re_path(r'^products/(?P<prod_id>\d+)/$', views.productdetail, name="productdetail"),
    path(r'place_order/',views.place_order,name='place_order'),
               ]
