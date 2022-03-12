from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField('Имя пользователя', max_length=200, null=True)
    email = models.CharField('Почта', max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    Detective = "Детектив"
    Science_fiction = "Фантастика"
    Adventures = "Приключения"
    Novel = "Роман"
    Scientific_book = "Научная книга"
    Folklore = "Фольклор"
    Humor = "Юмор"
    Reference_book = "Справочная книга"
    Poetry = "Поэзия"
    Children_book = "Детская книга"
    Documentary_literature = "Документальная литература"
    Business_literature = "Деловая литература"
    Religious_literature = "Религиозная литература"
    Educational_book = "Учебная книга"
    Books_about_psychology = "Книги о психологии"
    Hobby = "Хобби"
    Foreign = "Зарубежная"
    Equipment = "Техника"

    CHOISE_GROUP = {
        (Detective, "Детектив"),
        (Science_fiction, "Фантастика"),
        (Adventures, "Приключения"),
        (Novel, "Роман"),
        (Scientific_book, "Научная книга"),
        (Folklore, "Фольклор"),
        (Humor, "Юмор"),
        (Reference_book, "Справочная книга"),
        (Poetry, "Поэзия"),
        (Children_book, "Детская книга"),
        (Documentary_literature, "Документальная литература"),
        (Business_literature, "Деловая литература"),
        (Religious_literature, "Религиозная литература"),
        (Educational_book, "Учебная книга"),
        (Books_about_psychology, "Книги о психологии"),
        (Hobby, "Хобби"),
        (Foreign, "Зарубежная"),
        (Equipment, "Техника"),
    }

    name = models.CharField("Название книги", max_length=128)
    description = models.TextField("Описание книги")
    price = models.IntegerField("Цена")
    availability = models.BooleanField("Наличие", default = False)
    group = models.CharField("Жанр", max_length=100,choices=CHOISE_GROUP,default=Detective)
    img = models.ImageField("Обложка", default='Books_Shop_Site/no_image.jpg', upload_to='Books_Shop_Site/product_image')
    author = models.CharField("Автор книги", max_length = 256 )

    def _str_(self):
        return self.name_of_book

    @property
    def imgURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField('Дата оформления заказа',auto_now_add = True)
    complete = models.BooleanField('Статус',default = False)
    transaction_id = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.availability == True:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length = 200, null = False)
    city = models.CharField(max_length = 200, null = False)
    state = models.CharField(max_length = 200, null = False)
    zipcode = models.CharField(max_length = 200, null = False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
