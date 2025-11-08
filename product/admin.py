from django.contrib import admin
from .models import Category, Product, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_products_count']
    search_fields = ['name']
    
    def get_products_count(self, obj):
        return obj.products_count()
    get_products_count.short_description = 'Количество товаров'

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price', 'get_rating']
    list_filter = ['category']
    search_fields = ['title', 'description']
    list_editable = ['price']
    inlines = [ReviewInline]
    
    def get_rating(self, obj):
        return round(obj.rating(), 2)
    get_rating.short_description = 'Рейтинг'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'stars', 'text']
    list_filter = ['stars', 'product']
    search_fields = ['text']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)