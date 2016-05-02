from django.contrib import admin
from .models import Category, Subcategory, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'comment_required')


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Tag, TagAdmin)
