import csv

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Fills database from cdv file.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('csv_path', nargs='+', type=str)

    def handle(self, *args, **options):
        path_to_users_csv = ''.join((options['csv_path']))
        with open(path_to_users_csv) as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header

            User.objects.all().delete()

            User.objects.create_superuser(
                username='admin',
                email='',
                password='admin'
            )
            self.stdout.write(
                self.style.SUCCESS('CSV path: "%s"' % path_to_users_csv))
            for row in reader:
                self.stdout.write(
                    self.style.SUCCESS('Successfully added "%s"' % row))

                User.objects.create_user(
                    pk=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                )
