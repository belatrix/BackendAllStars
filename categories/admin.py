from django.contrib import admin
from .models import Category, Keyword


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'comment_required', 'is_active')


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Keyword, KeywordAdmin)
