# Generated by Django 3.0.6 on 2020-06-02 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20200512_0736'),
    ]

    operations = [
        migrations.CreateModel(
            name='CCEmails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]