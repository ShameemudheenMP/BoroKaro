from django.contrib import admin
from .models import *

# Register your models here.

# class ProdImageAdmin(admin.StackedInline):
#     model = ProdImage

# class ProdAdmin(admin.ModelAdmin):
#     inlines = [ProdImageAdmin]
#     list_display = ['p_name', 'p_rate', 'p_desc', 'month', 'year', 'status', 'rating']
#     class Meta:
#         model = Product

# admin.site.register(Product,ProdAdmin)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(PReq)
admin.site.register(Comment)
admin.site.register(ReportComment)
admin.site.register(ReportUser)