from csv import DictReader

from django.core.management import BaseCommand
# Import the model 
from reviews.models import Review, Title, User

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from review.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if Review.objects.exists():
            print('data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading data")


        #Code to load the data into database
        for row in DictReader(open('static/data/review.csv', encoding='utf-8')):
            review=Review(
                pk=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                score=row['score'],
                pub_date=row['pub_date'],
            )  
            review.save()
