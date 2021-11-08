from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(products)
admin.site.register(product_category)
admin.site.register(profile)
admin.site.register(Cart)