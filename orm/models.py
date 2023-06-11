from django.db import models
from django.db import connection

# --------------------------------- MANY TO MANY -----------------------------------
class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
    
    # @classmethod
    # def truncate(cls):
    #     with connection.cursor() as cursor:
    #         # sqlite commands
    #         cursor.execute('DELETE FROM {};'.format(cls._meta.db_table))
    #         cursor.execute('VACUUM;')

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publication_set = models.ManyToManyField(Publication, related_query_name='article_set')
    # By naming many to many field with _set suffix and setting 'related_query_name' with _set suffix,  I know both article_obj.publication_set.all() and
    # publication.obj.article_set.all() work and Article and Publication are ManyToMany-related to each other. Both Article.object.filter
    # (publication_set__tile__istartswith='Science') and Publication.objects.filter(article_set__pk=1) work, too.

    class Meta:
        ordering = ["headline"]

    def __str__(self):
        return self.headline
    
    # @classmethod
    # def truncate(cls):
    #     with connection.cursor() as cursor:
    #         cursor.execute('DELETE FROM {};'.format(cls._meta.db_table))
    #         cursor.execute('VACUUM;')
    


# --------------------------------- MANY TO ONE -----------------------------------

class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Report(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, related_name='reports', on_delete=models.CASCADE)
    # By set 'related_name' with 's' suffix or plural form,  It is clear to me this is a one to many relation.
    # reporter_obj.reports.all() or Reporter.objects.filter(reports__headline__icontains='This') works.

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ["headline"]

# --------------------------------- ONE TO ONE -----------------------------------
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name} the place"


class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name


class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='waiters', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)