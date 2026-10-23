from django.contrib import admin
from .models import Bill, BillSplit, Payment

admin.site.register(Bill)
admin.site.register(BillSplit)
admin.site.register(Payment)