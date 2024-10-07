from django.contrib import admin
from .models import Category, Flowers, FlowersType

admin.site.register(Category)
admin.site.register(FlowersType)
admin.site.register(Flowers)
