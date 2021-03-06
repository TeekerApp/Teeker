# Generated by Django 3.0.1 on 2020-01-26 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.BigIntegerField(unique=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=900)),
                ('url_path', models.URLField(unique=True)),
                ('amount_rating', models.BigIntegerField()),
                ('image_1', models.ImageField(help_text='Content Image 1', upload_to='uploaded_img/')),
                ('image_2', models.ImageField(help_text='Content Image 2', upload_to='uploaded_img/')),
                ('image_3', models.ImageField(help_text='Content Image 3', upload_to='uploaded_img/')),
                ('tags', models.TextField(max_length=1200)),
                ('category', models.CharField(max_length=500)),
            ],
        ),
    ]
