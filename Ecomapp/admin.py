from django.contrib import admin
from.models import*
#Register your models here.

admin.site.register(Category)

class ProductImageAdmin(admin.StackedInline):
    model=ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageAdmin]
admin.site.register(Product,ProductAdmin)

admin.site.register(Cart)
admin.site.register(Newproducts)
admin.site.register(Wishlist)    
admin.site.register(Order)
admin.site.register(Orderitem)    
admin.site.register(Profile)    
admin.site.register(Photo)    
admin.site.register(Video)    
admin.site.register(Brands)    
admin.site.register(Logo)    
admin.site.register(Orderhistory)    
admin.site.register(OrderTracker)  
admin.site.register(Blog)
  







admin.site.register(Category1)
admin.site.register(subCategory)

admin.site.register(Arrival)
admin.site.register(Demand)
admin.site.register(Delership)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Email', 'Phone', 'Message')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('Name2', 'Email2', 'Phone2', 'Product2', 'Message2')

@admin.register(Complaint)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('Name3', 'Email3', 'Phone3', 'Product3','Model3','Uploadbill3' ,'Message3')
 