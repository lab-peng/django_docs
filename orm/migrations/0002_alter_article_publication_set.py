# Generated by Django 4.2.1 on 2023-06-11 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publication_set',
            field=models.ManyToManyField(related_query_name='article_set', to='orm.publication'),
        ),
    ]
