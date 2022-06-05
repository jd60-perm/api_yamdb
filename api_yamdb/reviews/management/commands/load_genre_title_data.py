from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from reviews.models import Genre, Title


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from genre_title.csv"

    def handle(self, *args, **options):
    
        # Show this before loading the data into the database
        print("Loading data")


        #Code to load the data into database
        for row in DictReader(open('static/data/genre_title.csv', encoding='utf-8')):
            title=Title.objects.get(pk=row['title_id'])
            title.genre.add(Genre.objects.get(pk=row['genre_id']))
            title.save()
