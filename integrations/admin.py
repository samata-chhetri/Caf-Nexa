from django.contrib import admin
from .models import ExternalOrder, IntegrationLog

admin.site.register(ExternalOrder)
admin.site.register(IntegrationLog)