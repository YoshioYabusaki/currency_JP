from currency.models import ContactUs, GoodCafe, Rate, ResponseLog, Source
from currency.resources import ContactUsResource, GoodCafeResource, RateResource, ResponseLogResource, SourceResource

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
        'buy',
        'sale',
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
        'buy',
        'sale',
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


class ResponseLogAdmin(ImportExportModelAdmin):
    resource_class = ResponseLogResource
    list_display = (
        'id',
        'created',
        'status_code',
        'path',
        'response_time',
        'request_method',
    )
    list_filter = (
        ('created', DateRangeFilter),
    )
    readonly_fields = (  # запретить редактировать
        'id',
        'created',
        'status_code',
        'path',
        'response_time',
        'request_method',
    )

    def has_add_permission(self, request):  # запретить создать
        return False

    def has_delete_permission(self, request, obj=None):  # запретить удалть
        return False


admin.site.register(ResponseLog, ResponseLogAdmin)
