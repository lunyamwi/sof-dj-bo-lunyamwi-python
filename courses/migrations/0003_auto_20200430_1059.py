# Generated by Django 3.0.5 on 2020-04-30 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_article_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
