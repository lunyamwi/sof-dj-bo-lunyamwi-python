# Generated by Django 3.0.5 on 2020-04-30 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20200430_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=models.CharField(db_index=True, max_length=255), max_length=255),
        ),
    ]
