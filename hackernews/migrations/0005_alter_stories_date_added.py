# Generated by Django 4.1.1 on 2022-09-21 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0004_stories_text_alter_stories_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='date_added',
            field=models.DateTimeField(),
        ),
    ]
