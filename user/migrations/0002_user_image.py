# Generated by Django 3.0.4 on 2020-05-16 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profilephoto/%Y/%m/%d/'),
        ),
    ]
