from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import CustomUser
from poetry_translation.models import Poem


class Command(BaseCommand):
    help = "Generate a report of the number of users and poems."
    
    def handle(self, *args, **options):
        time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stdout.write("Usage report generated at", ending=" ")
        self.stdout.write(self.style.MIGRATE_HEADING(time))
        
        num_word_infos = Poem.objects.count()
        self.stdout.write("Total number of users:", ending=" ")
        self.stdout.write(self.style.SUCCESS(str(num_word_infos)))

        num_users = CustomUser.objects.count()
        self.stdout.write("Total number of poems:", ending=" ")
        self.stdout.write(self.style.SUCCESS(num_users))
        