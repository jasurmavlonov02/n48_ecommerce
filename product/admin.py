from django.contrib import admin
from product.models import Product, Attribute, AttributeValue, ProductAttribute

# Register your models here.


admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
