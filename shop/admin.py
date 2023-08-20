from django.contrib import admin
from .models import Product,Contact,Orders,orderupdate
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(orderupdate)

# Register your models here.
