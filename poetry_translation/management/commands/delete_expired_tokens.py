from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import CustomUserToken


class Command(BaseCommand):
    help = 'Deletes expired CustomUserToken instances'

    def handle(self, *args, **options):
        expired_tokens = CustomUserToken.objects.filter(expire_date__lte=timezone.now())
        expired_tokens.delete()

        self.stdout.write('Deleted expired tokens:', ending=' ')
        self.stdout.write(self.style.SUCCESS(str(expired_tokens.count())))
