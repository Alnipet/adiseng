from django.contrib import admin
from django.forms import ModelChoiceField

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    pass


class ManufacturerAdmin(admin.ModelAdmin):
    pass


class SeriesAdmin(admin.ModelAdmin):
    pass


class CartAdmin(admin.ModelAdmin):
    pass


class CartProductAdmin(admin.ModelAdmin):
    pass


class CustomerAdmin(admin.ModelAdmin):
    pass


class TemperatureSensorAdmin(admin.ModelAdmin):

    # фильтрация категории при добавлении товара
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='duct-temp-sensor'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FrequencyConverterAdmin(admin.ModelAdmin):

    # фильтрация категории при добавлении товара
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='fr-converter'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(TemperatureSensor, TemperatureSensorAdmin)
admin.site.register(FrequencyConverter, FrequencyConverterAdmin)
