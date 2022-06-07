from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Category, User, Title, Comment, Review, Genre


class Command(BaseCommand):
    help = "Loads data from all .csv"

    def handle(self, *args, **options):
            
        print("Loading data")

        for row in DictReader(open('static/data/users.csv', encoding='utf-8')):
            user=User(
                pk=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )  
            user.save()

        for row in DictReader(open('static/data/category.csv', encoding='utf-8')):
            category=Category(pk=row['id'], name=row['name'], slug=row['slug'])  
            category.save()

        for row in DictReader(open('static/data/genre.csv', encoding='utf-8')):
            genre=Genre(pk=row['id'], name=row['name'], slug=row['slug'])  
            genre.save()

        for row in DictReader(open('static/data/titles.csv', encoding='utf-8')):
            title=Title(pk=row['id'], name=row['name'], year=row['year'], category=Category.objects.get(pk=row['category']))  
            title.save()
        
        for row in DictReader(open('static/data/genre_title.csv', encoding='utf-8')):
            title=Title.objects.get(pk=row['title_id'])
            title.genre.add(Genre.objects.get(pk=row['genre_id']))
            title.save()

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

        for row in DictReader(open('static/data/comments.csv', encoding='utf-8')):
            comment=Comment(
                pk=row['id'],
                review=Review.objects.get(pk=row['review_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                pub_date=row['pub_date'],
            )  
            comment.save()
