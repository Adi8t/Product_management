from django.contrib import admin
from app.models import Category, Product, AuditLog, Review

admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')

admin.site.register(Product, ProductAdmin)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')

admin.site.register(AuditLog, AuditLogAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')

admin.site.register(Review, ReviewAdmin)
