from django.contrib import admin
from . models import customers
from . models import restaurants
from . models import delivery_guy
from . models import bill
from . models import menu
from . models import order


# Register your models here.


admin.site.register(customers)
admin.site.register(restaurants)
admin.site.register(delivery_guy)
admin.site.register(bill)
admin.site.register(menu)
admin.site.register(order)