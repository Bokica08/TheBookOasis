from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from TheBookOasis.forms import CustomAuthenticationForm, SearchForm, DeliveryInfoForm, RegisterForm, BookForm, \
    UpdateQuantityForm
from TheBookOasis.models import ShoppingCart, Book, Category, ShoppingCartItem, Order


# Create your views here.
def welcome(request):
    return render(request, "welcome.html")


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            cart = ShoppingCart.objects.filter(
                user=form.get_user()).first()
            if not cart:
                createNewShoppingCart(form.get_user())
            return redirect('/home/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def createNewShoppingCart(current_user):
    cart = ShoppingCart(user=current_user)
    cart.save()


def home(request):
    books = Book.objects.all()[:4]
    return render(request, "home.html", context={"books": books})

def categories(request):
    categories= Category.objects.all()
    return render(request,'categories.html',context={"categories":categories})
def search_view(request):
    form = SearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        if search_query:
            books = books.filter(name__icontains=search_query)

    if 'clear' in request.GET:
        form = SearchForm()
        books = Book.objects.all()

    context = {
        'form': form,
        'books': books
    }

    return render(request, 'books.html', context)
def getSCUser(request):
    return ShoppingCart.objects.all().filter(user=request.user).first()
def book_details_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    isInShoppingCart = False
    if request.user.is_authenticated:
        shoppingCart = getSCUser(request)
        items = ShoppingCartItem.objects.all().filter(shoppingCart=shoppingCart)
        for item in items:
            if item.book == book:
                isInShoppingCart = True
                break

    context = {
        'book': book,
        'isInShoppingCart': isInShoppingCart,
    }
    return render(request, 'details.html', context)

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category=category)

    context = {
        'category': category,
        'books': books
    }

    return render(request, 'category_books.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')


def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    quantity = request.POST.get('quantity')
    if book.quantity < int(quantity):
        return render(request, 'details.html', {'book': book, 'quantity': quantity})
    else:
        item = ShoppingCartItem(book=book, quantity=quantity, shoppingCart=ShoppingCart.objects.all().filter(
            user=request.user).first())
        item.save()
        book.quantity -= int(quantity)
        book.save()
        return redirect('book_details', book_id=pk)

def cart(request):
    if request.user.is_authenticated:
        shoppingCart = getSCUser(request)
        items = ShoppingCartItem.objects.all().filter(shoppingCart=shoppingCart)
        total = sum([item.subtotal() for item in items])
        return render(request, 'cart.html', {
            'shoppingCart': shoppingCart,
            'items': items,
            'total': total
        })
    return redirect('/login/')
def deleteFromCart(request, pk):
    item = get_object_or_404(ShoppingCartItem, pk=pk)
    book = item.book
    book.quantity += item.quantity
    book.save()
    item.delete()
    return redirect('/cart/')

def deliveryInfo(request):
    if request.user.is_authenticated:
        shoppingCart = getSCUser(request)
        items = ShoppingCartItem.objects.all().filter(shoppingCart=shoppingCart)
        total = sum([item.subtotal() for item in items])
        form = DeliveryInfoForm()
        if request.method == 'POST':
            form = DeliveryInfoForm(request.POST)
            order = Order(user=request.user, cart=getSCUser(request),
                      total=total, date=datetime.now())
            order.save()
            if form.is_valid():
                delivery = form.save(commit=False)
                delivery.order = order
                delivery.save()
                items =  ShoppingCartItem.objects.all().filter(shoppingCart=order.cart)
                for item in items:
                    book = item.book
                    book.save()
                shoppingCart =  ShoppingCart.objects.all().filter(user=request.user).first()
                shoppingCart.user = None
                shoppingCart.save()
                createNewShoppingCart(request.user)
                return redirect('оrderSuccess')
        return render(request, 'deliveryInfo.html', {
            'form': form,
            'total': total
        })
    return redirect('/login/')

def orderSuccess(request):
    return render(request, 'orderSuccess.html')

def myOrders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        items = ShoppingCartItem.objects.filter(shoppingCart__order__in=orders).values('book__name').annotate(total_quantity=Sum('quantity'))
        return render(request, 'myOrders.html', {
            'orders': orders,
            'items': items,
        })
    return redirect('/login/')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_page')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def loginAdmin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('/home/')
            else:
                messages.error(request, 'Не сте авторизирани за администраторска најава.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'adminLogin.html', {'form': form})

def addBook(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('successfullAddBook')
    else:
        form = BookForm()
    return render(request, 'addBook.html', {'form': form})

def update_quantity(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        form = UpdateQuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Update the quantity of the book
            book.quantity = quantity
            book.save()
            return redirect('book_details', book_id=book.id)
    else:
        form = UpdateQuantityForm()

    return render(request, 'updateQuantity.html', {'form': form, 'book': book})

def successfullAddBook(request):
    return render(request, 'successfullAddBook.html')

def allOrders(request):
    orders = Order.objects.all()
    return render(request, 'allOrders.html', {'orders': orders})

def change_order_status(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status='Deliver'
    order.save()
    return redirect('allOrders')