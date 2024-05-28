# Generated by Django 4.2.13 on 2024-05-13 19:03

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('researchdata', '0002_initial_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialmediaplatform',
            options={'ordering': [django.db.models.functions.text.Upper('name'), 'id'], 'verbose_name': 'digital platform'},
        ),
        migrations.AlterModelOptions(
            name='socialmediapost',
            options={'ordering': ['id'], 'verbose_name': 'post'},
        ),
        migrations.AlterModelOptions(
            name='socialmediapostimage',
            options={'ordering': ['id'], 'verbose_name': 'post image'},
        ),
        migrations.AddField(
            model_name='socialmediapost',
            name='content_video_other',
            field=models.CharField(blank=True, help_text='If the video is in a format other than YouTube or Vimeo please include a URL to the video here', max_length=1000, null=True, verbose_name='content video (other)'),
        ),
        migrations.AlterField(
            model_name='author',
            name='social_media_profiles',
            field=models.TextField(blank=True, help_text='List the URL for each social media profile for this Author on a new line in the text box', null=True, verbose_name='digital profiles'),
        ),
    ]
