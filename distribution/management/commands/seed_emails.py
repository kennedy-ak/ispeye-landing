from django.core.management.base import BaseCommand
from distribution.models import ApprovedEmail

INITIAL_EMAILS = [
    ('sikabee66@gmail.com', 'Play Console tester'),
    ('adabsroot@gmail.com', 'Play Console tester'),
    ('addy4h@gmail.com', 'Play Console tester'),
    ('dorothyquist20@gmail.com', 'Play Console tester'),
    ('eb.adutwum@gmail.com', 'Play Console tester'),
    ('emmanuellaankomah596@gmail.com', 'Play Console tester'),
    ('iammiyamuhammed@gmail.com', 'Play Console tester'),
    ('michellenankabruce@gmail.com', 'Play Console tester'),
    ('naalamleboye@gmail.com', 'Play Console tester'),
    ('nicolenankabruce@gmail.com', 'Play Console tester'),
    ('osaeroselyne@gmail.com', 'Play Console tester'),
    ('svendzeble1@gmail.com', 'Play Console tester'),
    ('cyrusaddy90@gmail.com', 'Admin'),
    ('belmontsolutionsgh@gmail.com', 'Admin'),
]


class Command(BaseCommand):
    help = 'Load initial approved emails (Play Console testers + admins)'

    def handle(self, *args, **kwargs):
        created = 0
        for email, note in INITIAL_EMAILS:
            _, was_created = ApprovedEmail.objects.get_or_create(
                email=email,
                defaults={'note': note}
            )
            if was_created:
                created += 1
                self.stdout.write(f'  Added: {email}')
        self.stdout.write(self.style.SUCCESS(f'\nDone. Created {created} new approved email(s).'))
