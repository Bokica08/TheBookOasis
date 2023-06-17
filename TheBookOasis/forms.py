from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from TheBookOasis.models import DeliveryInfo, Author, Category, Book


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'


class SearchForm(forms.Form):
    search_query = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control w-100', 'placeholder': 'Пребарај книга'}))


class DeliveryInfoForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control mb-3 inline-form-field'
            })


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_class = 'form-control'

        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields[
            'password1'].help_text = ''
        self.fields['password2'].help_text = ''

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': bootstrap_class, 'placeholder': ''})


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'category', 'details', 'photo', 'price', 'quantity']

    name = forms.CharField(label='Име', required=True)
    author = forms.ModelChoiceField(label='Автор', queryset=Author.objects.all(), required=True)
    category = forms.ModelChoiceField(label='Категорија', queryset=Category.objects.all(), required=True)
    details = forms.CharField(label='Опис', widget=forms.Textarea, required=True)
    photo = forms.ImageField(label='Слика', required=True)
    price = forms.IntegerField(label='Цена', required=True)
    quantity = forms.IntegerField(label='Количина', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_class = 'form-control'

        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': bootstrap_class})


class UpdateQuantityForm(forms.Form):
    quantity = forms.IntegerField(label='Количина', widget=forms.TextInput(attrs={'class': 'form-control'}))
