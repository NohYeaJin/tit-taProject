from django.contrib import admin
from .models import Musicals, Categories, Locations, Genres, MainImages

class CrawledMusicalAdmin(admin.ModelAdmin):
    search_fields = ['title', 'ticket_attribute', 'prf_attribute', 'search_keyword']
    list_filter = ['category', 'theater', 'cast', 'price', 'open_from', 'open_to']
    readonly_fields = ['img_preview']

class MainImageAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']

admin.site.register(Musicals, CrawledMusicalAdmin)
admin.site.register(Categories)
admin.site.register(Locations)
admin.site.register(Genres)
admin.site.register(MainImages, MainImageAdmin)