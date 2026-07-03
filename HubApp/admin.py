from django.contrib import admin
from.models import *

# Register your models here.
admin.site.register(users)
admin.site.register(products)
admin.site.register(orders)
admin.site.register(cart)
admin.site.register(Category)


