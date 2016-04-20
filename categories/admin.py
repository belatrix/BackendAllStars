from django.contrib import admin
from .models import Category, Subcategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight',)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
