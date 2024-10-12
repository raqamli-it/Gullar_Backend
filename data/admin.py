from django.contrib import admin
from .models import Category, CategoryType,  Flowers, FlowersType, News

admin.site.register(Category)
admin.site.register(CategoryType)
admin.site.register(FlowersType)
admin.site.register(Flowers)
admin.site.register(News)
