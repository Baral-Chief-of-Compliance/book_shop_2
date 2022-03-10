from django.contrib import admin
from django.utils.safestring import mark_safe
from store.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "author", "get_image")
    list_filter = ("name", "group", "author")
    search_fields = ("name", "group", "author")

    def get_image(self, obj):
        return mark_safe(f'<img src ={obj.img.url} width="100"  height = "120">')


admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
