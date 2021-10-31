from currency.models import Rate
from currency.tasks import parse_privatbank_archive

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Parse Privatbank Rate archive' # noqa

    def handle(self, *args, **options):
        print(  # noqa
            'Count:', Rate.objects.count(), '-->>',
            parse_privatbank_archive(),
            'New Count:', Rate.objects.count(),
        )
# -->> $ python ./app/manage.py parse_privatbank_archive
