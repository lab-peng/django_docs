from django.core.management.base import BaseCommand
from aggregation.models import Author, Publisher, Book, Store
from orm.models import Publication, Article
from datetime import date

from django.db.models import Avg, Max, Min, Count, Sum, Q
from django.db import models

from django.utils import timezone


def insert_data():
    Author.objects.create(name='Kurt Vonnegut', age=95)
    Author.objects.create(name='George Orwell', age=135)
    Author.objects.create(name='Rachel Caine', age=35)
    Author.objects.create(name='Ann Aguirre', age=27)
    
    Publisher.objects.create(name='Random House')
    Publisher.objects.create(name='Simon & Schuster')

    Book.objects.create(
        name = 'God bless you, Mr. Rosewater',
        pages = 125,
        price = 25.36,
        rating = 8.7,
        publisher = Publisher.objects.first(),
        pubdate = '2023-05-23',
    )
    Book.objects.create(
        name = 'Animal Farm',
        pages = 87,
        price = 15.20,
        rating = 9.7,
        publisher = Publisher.objects.first(),
        pubdate = '2023-05-21',
    )
    Book.objects.create(
        name = 'Slaughterhouse-Five',
        pages = 138,
        price = 15.20,
        rating = 8.2,
        publisher = Publisher.objects.first(),
        pubdate = '2023-05-21',
    )
    Book.objects.create(
        name = 'Timequake',
        pages = 138,
        price = 8.20,
        rating = 3.2,
        publisher = Publisher.objects.first(),
        pubdate = '2023-05-21',
    )
    Book.objects.create(
        name = 'Honor Among Thieves',
        pages = 138,
        price = 8.20,
        rating = 3.2,
        publisher = Publisher.objects.last(),
        pubdate = '2023-05-21',
    )

    Book.objects.get(name='God bless you, Mr. Rosewater').authors.add(Author.objects.get(name='Kurt Vonnegut'))
    Book.objects.get(name='Slaughterhouse-Five').authors.add(Author.objects.get(name='Kurt Vonnegut'))
    Book.objects.get(name='Timequake').authors.add(Author.objects.get(name='Kurt Vonnegut'))
    Book.objects.get(name='Animal Farm').authors.add(Author.objects.get(name='George Orwell'))
    Book.objects.get(name='Honor Among Thieves').authors.add(Author.objects.get(name='Rachel Caine'), Author.objects.get(name='Ann Aguirre'))

    names = ['Olivia', 'Emma', 'Charlotte', 'Amelia', 'Sophia', 'Isabella', 'Ava', 'Mia']
    for n in names:
        Store.objects.create(name=n + "'s")

def query_data():
    avg_book_price = Book.objects.aggregate(Avg("price", output_field=models.FloatField()))
    max_book_price = Book.objects.aggregate(Max('price'))
    min_book_price = Book.objects.aggregate(Min('price'))
    max_avg_diff = Book.objects.aggregate(price_diff=Max("price") - Avg("price"))
    print(avg_book_price, max_book_price, min_book_price, max_avg_diff)

    print()
    print(Book.objects.aggregate(Avg("price"), Max("price"), Min("price")))

    print()
    pubs = Publisher.objects.annotate(num_books=Count("book"))
    for pub in pubs:
        print(pub.num_books)

    print()
    above_5 = Count('book', filter=Q(book__rating__gt=5))
    below_5 = Count('book', filter=Q(book__rating__lt=5))
    pubs = Publisher.objects.annotate(below_5=below_5).annotate(above_5=above_5)
    for pub in pubs:
        print(pub.above_5, pub.below_5)

    print()
    pubs = Publisher.objects.annotate(num_books=Count("book")).order_by("-num_books")[:5]
    for pub in pubs:
        print(pub.num_books)

    print()
    # books = Book.objects.annotate(Count('authors'))
    books = Book.objects.annotate(num_authors=Count('authors'))
    for b in books:
        # print(b.authors__count)
        print(b.num_authors)

    print()
    # ❌ books = Book.objects.annotate(Count('authors'), Count('store'))
    books = Book.objects.annotate(Count('authors', distinct=True), Count('store', distinct=True))
    for b in books:
        print(b.authors__count, b.store__count)

    print()
    stores = Store.objects.annotate(min_price=Min("books__price"), max_price=Max("books__price"))
    for s in stores:
        print(s.min_price, s.max_price)
    print(Store.objects.aggregate(min_price=Min("books__price", output_field=models.FloatField()), max_price=Max("books__price", output_field=models.FloatField())))
    print(Store.objects.aggregate(youngest_age=Min("books__authors__age")))

    print()
    pubs = Publisher.objects.annotate(Count("book"))
    for p in pubs:
        print(p.book__count)
    print(Publisher.objects.aggregate(oldest_pubdate=Min("book__pubdate")))
    authors = Author.objects.annotate(total_pages=Sum("book__pages"))
    for a in authors:
        print(a.name, a.total_pages)
    print(Author.objects.aggregate(average_rating=Avg("book__rating")))

    print()
    books =  Book.objects.filter(name__icontains='s').annotate(num_authors=Count("authors"))
    for b in books:
        print(b.name, b.num_authors, b.authors.all(), b.price)
    print(Book.objects.filter(name__icontains='s').aggregate(Avg('price', output_field=models.FloatField())))
    books = Book.objects.annotate(num_authors=Count("authors")).filter(num_authors__gt=1)
    for b in books:
        print(b.name, b.num_authors)
    highly_rated = Count("book", filter=Q(book__rating__gte=7))
    authors = Author.objects.annotate(num_books=Count("book"), highly_rated_books=highly_rated)
    for a in authors:
        print(a.name, a.num_books, a.highly_rated_books)


    print()
    books = Book.objects.annotate(num_authors=Count("authors")).order_by("-num_authors")
    for b in books:
        print(b.name, b.num_authors)
    print(Author.objects.annotate(average_rating=Avg('book__rating')))
    print(Author.objects.values("name").annotate(average_rating=Avg("book__rating")))
    print(type(books), books.explain())

def query_data_raw():
    for b in Book.objects.raw('SELECT * FROM aggregation_book'):
        print(b)

    name_map = {
        'name': 'title',
        'price': 'value'
    }
    books = Book.objects.raw('SELECT * FROM aggregation_book', translations=name_map)
    for b in books:
        print(b.title, b.value)

    first_author = Author.objects.raw("SELECT * FROM aggregation_author LIMIT 1")[0]
    print(first_author)

    print()
    name = 'Kurt Vonnegut'
    kurt_vonnegut = Author.objects.raw(
        'SELECT id, name from aggregation_author where name LIKE %s', [name]
        )[0]
    print(kurt_vonnegut.name, kurt_vonnegut.age)

    name = 'A'
    books = Book.objects.raw(
        'SELECT id, name from aggregation_book where name = %s', [name]
    )
    for b in books:
        print(b)
    # TODO why LIKE = %s DOES NOT work?



def insert_data_orm():
    p1 = Publication(title="The Python Journal")
    p1.save()
    p2 = Publication(title="Science News")
    p2.save()
    p3 = Publication(title="Science Weekly")
    p3.save()

    a1 = Article(headline="Django lets you build web apps easily")
    a1.save()
    a1.publication_set.add(p1)

    a2 = Article(headline="NASA uses Python")
    a2.save()
    a2.publication_set.add(p1, p2)
    a2.publication_set.add(p3)

    # Create and add a Publication to an Article in one step using create()
    a2 = Article.objects.get(pk=2)
    p4 = a2.publication_set.create(title="Highlights for Children")

    p2 = Publication.objects.get(pk=2)
    a3 = p2.article_set.create(headline="Oxygen-free diet works wonders")


def query_data_orm():
    a1 = Article.objects.get(headline='Django lets you build web apps easily')
    print(a1.publication_set.all())

    a2 = Article.objects.get(pk=2)
    print(a2.publication_set.all())
    print(a2.publication_set.filter(title__icontains='science'))
    print(Article.objects.filter(publication_set__title__istartswith='science'))
    print(Article.objects.filter(publication_set__title__istartswith='science').count())
    print(Article.objects.filter(publication_set__title__istartswith='science').distinct())
    print(Article.objects.filter(publication_set__title__istartswith='science').distinct().count())
    
    p1 = Publication.objects.get(title='The Python Journal')
    print(p1.article_set.all())
    print(p1.article_set.filter(headline__icontains='NASA'))

    # The below 4 queries are exactly the same
    print(Article.objects.filter(publication_set__id=1))
    print(Article.objects.filter(publication_set__pk=1))
    print(Article.objects.filter(publication_set=1))
    print(Article.objects.filter(publication_set=p1))

    print(Article.objects.filter(publication_set__in=[1, 2]).distinct())
    p2 = Publication.objects.get(pk=2)
    print(Article.objects.filter(publication_set__in=[p1, p2]).distinct())

    # Reverse queries
    print(Publication.objects.filter(article_set__headline__startswith="NASA"))
    print(Publication.objects.filter(article_set__id=1))
    print(Publication.objects.filter(article_set__pk=1))
    print(Publication.objects.filter(article_set=1))
    print(Publication.objects.filter(article_set=a1))

    print(Publication.objects.filter(article_set__in=[1, 2]).distinct())
    print(Publication.objects.filter(article_set__in=[a1, a2]).distinct())

    print(Article.objects.exclude(publication_set=p2))

    print(p2.article_set.all())
    a3 = p2.article_set.all()[1]
    print(a3)
    print(a3.publication_set.all())

    
    

    
# TODO django async aggregate and others 
# async def get_max_avg_diff():
#     await Book.objects.aaggregate(price_diff=Max('price', output_field=models.FloatField()) - Avg('price'))
    

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        pass
        # insert_data()
        # query_data()
        # query_data_raw()
        # print(timezone.get_current_timezone_name())

        # insert_data_orm()
        query_data_orm()












    