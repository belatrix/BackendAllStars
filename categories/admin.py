from django.contrib import admin
from .models import Category, Keyword, Subcategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'comment_required', 'is_active')


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Keyword, KeywordAdmin)
