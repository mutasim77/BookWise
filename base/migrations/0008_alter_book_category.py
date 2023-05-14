# Generated by Django 4.1.6 on 2023-04-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(default=None, help_text='The category of the book.', max_length=70),
        ),
    ]