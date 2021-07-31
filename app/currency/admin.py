from currency.models import ContactUs, GoodCafe, Rate, Source
from currency.resources import ContactUsResource, GoodCafeResource, RateResource, SourceResource

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from rangefilter.filters import DateRangeFilter


class ContactUsAdmin(admin.ModelAdmin):
    resource_class = ContactUsResource
    list_display = (
        'id',
        'user_name',
        'email_form',
        'subject',
        'message',
        'created',
    )
    list_filter = (
        ('created', DateRangeFilter),
    )
    search_fields = (
        'user_name',
        'email_form',
        'subject',
        'message',
    )
    readonly_fields = (  # запретить редактировать
        'id',
        'user_name',
        'email_form',
        'subject',
        'message',
        'created',
    )

    def has_add_permission(self, request):  # запретить создать
        return False

    def has_delete_permission(self, request, obj=None):  # запретить удалть
        return False

admin.site.register(ContactUs, ContactUsAdmin)


class RateAdmin(ImportExportModelAdmin):
    resource_class = RateResource
    list_display = (
        'id',
        'source',
        'type',
        'sale',
        'buy',
        'created',
    )
    list_filter = (
        'type',
        'source',
        ('created', DateRangeFilter),
    )
    search_fields = (
        'type',
        'source',
    )
    readonly_fields = (
        'sale',
        'buy',
    )

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Rate, RateAdmin)


class SourceAdmin(ImportExportModelAdmin):
    resource_class = SourceResource
    list_display = (
        'id',
        'name',
        'source_url',
    )
    search_fields = (
        'name',
        'source_url',
    )

admin.site.register(Source, SourceAdmin)


class GoodCafeAdmin(ImportExportModelAdmin):
    resource_class = GoodCafeResource
    list_display = (
        'id',
        'cafe_name',
        'open_time',
        'close_time',
        'address',
        'recommended_menu',
    )
    search_fields = (
        'cafe_name',
        'address',
        'recommended_menu',
    )

admin.site.register(GoodCafe, GoodCafeAdmin)
