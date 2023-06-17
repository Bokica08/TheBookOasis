"""D5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from D5 import settings
from TheBookOasis.views import welcome, login_page, home, categories, search_view, book_details_view, category_view, \
    logout_view, add_to_cart, cart, deleteFromCart, deliveryInfo, orderSuccess, myOrders, register, loginAdmin, addBook, \
    update_quantity, successfullAddBook, allOrders, change_order_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',welcome,name="welcome"),
    path('login/',login_page,name="login_page"),
    path('home/',home,name="home"),
    path('categories/',categories,name="categories"),
    path('books/',search_view,name="search_view"),
    path('books/<int:book_id>/', book_details_view, name='book_details'),
    path('category/<str:category_id>/', category_view, name='category'),
    path('logout/', logout_view, name='logout'),
    path('books/<int:pk>/add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/',cart,name="cart"),
    path('deleteFromCart/<int:pk>/', deleteFromCart, name='deleteFromCart'),
    path('deliveryInfo/', deliveryInfo, name='deliveryInfo'),
    path('order/success/', orderSuccess, name='оrderSuccess'),
    path('myOrders/', myOrders, name='myOrders'),
    path('register/',register,name="register"),
    path('adminLogin/',loginAdmin,name="loginAdmin"),
    path('addBook/',addBook,name="addBook"),
    path('update_quantity/<int:book_id>/', update_quantity, name='update_quantity'),
    path('successfullAddBook/',successfullAddBook,name="successfullAddBook"),
    path('allOrders/',allOrders,name="allOrders"),
    path('orders/change_status/<int:order_id>/', change_order_status, name='change_order_status'),

]+static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
