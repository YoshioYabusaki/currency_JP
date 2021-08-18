from currency.models import ContactUs, GoodCafe, Rate, ResponseLog, Source

from import_export import resources


class ContactUsResource(resources.ModelResource):

    class Meta:
        model = ContactUs
        fields = (
            'id',
            'user_name',
            'email_form',
            'subject',
            'message',
            'created',
        )


class RateResource(resources.ModelResource):

    class Meta:
        model = Rate
        fields = (
            'id',
            'source',
            'type',
            'sale',
            'buy',
            'created',
        )


class SourceResource(resources.ModelResource):

    class Meta:
        model = Source
        fields = (
            'id',
            'name',
            'source_url',
        )


class GoodCafeResource(resources.ModelResource):

    class Meta:
        model = GoodCafe
        fields = (
            'id',
            'cafe_name',
            'open_time',
            'close_time',
            'address',
            'recommended_menu',
        )


class ResponseLogResource(resources.ModelResource):

    class Meta:
        model = ResponseLog
        fields = (
            'id',
            'created',
            'status_code',
            'path',
            'response_time',
            'request_method',
        )
