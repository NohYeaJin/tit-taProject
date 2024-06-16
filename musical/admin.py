from django.contrib import admin
from .models import Musicals, Categories, Locations, Genres, MainImages, Notice, PushNotification, MusicalSeries, \
    MusicalSource, TicketNotification, Users, MusicalReservationLink


class CrawledMusicalAdmin(admin.ModelAdmin):
    search_fields = ['title', 'ticket_attribute', 'prf_attribute', 'search_keyword']
    list_filter = ['category', 'theater', 'cast', 'price', 'open_from', 'open_to']
    readonly_fields = ['img_preview']

class MainImageAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']

class TicketNotificationAdmin(admin.ModelAdmin):
    readonly_fields = ['musical_id', 'user_id', 'created_at']

@admin.register(Notice)
class QuillPostAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_email', 'user_phone', 'user_address', 'user_nickname', 'user_last_login')
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Musicals, CrawledMusicalAdmin)
admin.site.register(Categories)
admin.site.register(Locations)
admin.site.register(Genres)
admin.site.register(MainImages, MainImageAdmin)
admin.site.register(PushNotification)
admin.site.register(MusicalSeries)
admin.site.register(MusicalSource)
admin.site.register(TicketNotification, TicketNotificationAdmin)
admin.site.register(Users, UserAdmin)
admin.site.register(MusicalReservationLink)

