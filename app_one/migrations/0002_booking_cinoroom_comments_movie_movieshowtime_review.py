# Generated by Django 2.2 on 2020-07-28 07:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('likes', models.ManyToManyField(related_name='has_likes', to='app_one.User')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_movies', to='app_one.User')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_reviews', to='app_one.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_one.User')),
            ],
        ),
        migrations.CreateModel(
            name='MovieShowTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('showtime', models.ManyToManyField(related_name='showtime', to='app_one.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='app_one.Movie')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_comments', to='app_one.User')),
            ],
        ),
        migrations.CreateModel(
            name='CinoRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3')], default='A1', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_room', to='app_one.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tickets', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_tickets', to='app_one.User')),
                ('cino_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='app_one.CinoRoom')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_tickets', to='app_one.Movie')),
            ],
        ),
    ]
