from django.contrib import admin
from .models import *
# Register your models here.





class CardAdmin(admin.ModelAdmin):
    '''Admin View for '''

    list_display = ('title','date_now','text')
    list_filter = ('date_now',)
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ("text", "title")
    # date_hierarchy = ''
    ordering = ('title',)

class SepetAdmin(admin.ModelAdmin):
    '''Admin View for '''

    list_display = ('user','product', 'price', 'adet','id')
    

admin.site.register(Card, CardAdmin)
admin.site.register(Category)
admin.site.register(Comments) 
admin.site.register(Sepet, SepetAdmin)
