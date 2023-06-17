from django.contrib import admin

from TheBookOasis.models import Book, Category, Author, ShoppingCart, ShoppingCartItem, DeliveryInfo, Order


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Book, BookAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Category, CategoryAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Author, AuthorAdmin)

admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(DeliveryInfo)
admin.site.register(Order)
