# Generated by Django 3.0.4 on 2020-05-16 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InternautPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_posted', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('reported', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=8)),
                ('content', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='vedios')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WriterPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_posted', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('reported', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=8)),
                ('content', models.TextField()),
                ('file', models.FileField(default='N/A', upload_to='media')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
