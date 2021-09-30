from currency.models import ContactUs, Rate, Source
from currency.tasks import contact_us

from rest_framework import serializers


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            'id',
            'created',
            'user_name',
            'email_form',
            'subject',
            'message',
        )

    def create(self, validated_data):
        instance = ContactUs.objects.create(**validated_data)
        full_email_body = f'''
                *** Sent from API ***
                User Name: {instance.user_name}
                Email from: {instance.email_form}
                Subject: {instance.subject}
                Body: {instance.message}
                '''
        contact_us.apply_async(args=(instance.subject, ), kwargs={'body': full_email_body})
        return instance


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'name',
        )


class RateSerializer(serializers.ModelSerializer):
    source_obj = SourceSerializer(source='source', read_only=True)

    class Meta:
        model = Rate
        fields = (
            'id',
            'source_obj',  # GETのときだけ
            'source',  # POSTのときだけ
            'type',
            'buy',
            'sale',
            'created',
        )
        extra_kwargs = {
            'source': {'write_only': True},
        }


class SourceWithRateSerializer(serializers.ModelSerializer):
    rate_set = RateSerializer(many=True, source='rates', read_only=True)

    class Meta:
        model = Source
        fields = (
            'id',
            'name',
            'rate_set',
        )
