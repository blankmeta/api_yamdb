from users.models import User
import csv


def fill_users():
    with open('static/data/users.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        User.objects.all().delete()

        User.objects.create_superuser(
            username='admin',
            password='admin'
        )

        for row in reader:
            print(row)

            User.objects.create_user(
                pk=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6],
            )
