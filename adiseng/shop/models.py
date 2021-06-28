from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


# Category
# Product
# CartProduct
# Cart
# Customer
# Order


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatestProducts:

    objects = LatestProductsManager()


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Категория',
    )

    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Категория',
    )

    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Серия',
    )

    manufacturer = models.ForeignKey(
        'Manufacturer',
        verbose_name='Производитель',
        on_delete=models.CASCADE,
    )

    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )

    manufacturer = models.ForeignKey(
        'Manufacturer',
        verbose_name='Производитель',
        on_delete=models.CASCADE,
    )

    series = models.ForeignKey(
        'Series',
        verbose_name='Серия',
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=150,
        verbose_name='Наименование',
    )

    slug = models.SlugField(
        unique=True,
    )

    image = models.ImageField(
        blank=True,
    )

    description = models.TextField(
        verbose_name='Описание',
        null=True, #почему?
    )

    manual_doc = models.FileField(
        verbose_name='Руководство',
        blank=True,
    )

    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    customer = models.ForeignKey(
        'Customer',
        verbose_name='Заказчик',
        on_delete=models.CASCADE,
    )

    cart = models.ForeignKey(
        'Cart',
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        related_name='related_products'
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField(
    )

    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    qty = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    total_price = models.DecimalField(
        verbose_name='Общая цена',
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return 'Товар: {}'.format(self.content_object)


class Cart(models.Model):
    owner = models.ForeignKey(
        'Customer',
        verbose_name='Владелец корзины',
        on_delete=models.CASCADE,
    )

    products = models.ManyToManyField(
        CartProduct,
        blank=True,
        related_name='related_cart'
    )

    total_products = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество товаров',
    )

    total_price = models.DecimalField(
        verbose_name='Итоговая цена',
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=12,
        verbose_name='Номер телефона',
    )

    company = models.CharField(
        max_length=255,
        verbose_name='Название компании',
    )

    legal_address = models.CharField(
        max_length=255,
        verbose_name='Юридический адрес',
    )

    actual_address = models.CharField(
        max_length=255,
        verbose_name='Фактический адрес',
    )

    def __str__(self):
        return self.company


class TemperatureSensor(Product):
    """
    Датчики температуры (термосопротивления)
    """

    temp_range = models.CharField(
        max_length=15,
        verbose_name='Диапазон измерения температуры',
    )

    operating_temp = models.CharField(
        max_length=15,
        verbose_name='Температура эксплуатации',
        blank=True,
    )

    measure_error = models.CharField(
        max_length=15,
        verbose_name='Погрешность измерений',
        blank=True,
    )

    ip_connect = models.CharField(
        max_length=15,
        verbose_name='Пыле- и влагозащита со стороны подключения',
        blank=True,
    )

    ip_sensor = models.CharField(
        max_length=15,
        verbose_name='Пыле- и влагозащита измерительного элемента',
        blank=True,
    )

    probe_material = models.CharField(
        max_length=15,
        verbose_name='Материал сенсора',
        blank=True,
    )

    sensor = models.CharField(
        max_length=15,
        verbose_name='Измерительный элемент',
        blank=True,
    )

    sensor_length = models.CharField(
        max_length=15,
        verbose_name='Длина измерительного элемента',
        blank=True,
    )

    def __str__(self):
        return "{} / {}".format(self.title, self.category)


class FrequencyConverter(Product):
    """
    Частотные преобразователи
    """

    power = models.CharField(
        max_length=15,
        verbose_name='Мощность',
    )

    current = models.CharField(
        max_length=15,
        verbose_name='Ток',
    )

    voltage = models.CharField(
        max_length=15,
        verbose_name='Напряжение',
    )

    ip_case = models.CharField(
        max_length=15,
        verbose_name='Пыле- и влагозащита корпуса',
    )

    def __str__(self):
        return "{} / {}".format(self.title, self.category)
