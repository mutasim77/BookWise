# Generated by Django 4.1.6 on 2023-04-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_book_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.CharField(help_text='Price of book', max_length=10),
        ),
    ]
