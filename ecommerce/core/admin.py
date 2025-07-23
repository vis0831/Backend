from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Order

# Show image preview in admin
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_active', 'category', 'image_tag']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'description']
    
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email']

admin.site.register(Order, OrderAdmin)
