from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return self.name + " " + self.surname


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    details = models.TextField()
    photo = models.ImageField(upload_to="data/")
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)


class ShoppingCartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.book.name + " " + str(self.quantity)

    def subtotal(self):
        return self.book.price * self.quantity


class DeliveryInfo(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    addressNumber = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    payment = models.CharField(max_length=100,
                               choices=([('Delivery', 'Наплата при достава'), ('Card', 'Наплата со картичка')]))


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    total = models.IntegerField()
    status = models.CharField(max_length=100,
                               choices=([('Processing', 'Се процесира'), ('Deliver', 'Испратена на адреса')]),default='Processing')

    def __str__(self):
        return self.user.username + " " + str(self.date) + " " + str(self.total)
