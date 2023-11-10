from django.conf import settings
from django.db import migrations
from researchdata import models


def insert_data_country(apps, schema_editor):
    """
    Inserts default data into the Country model
    """

    for name in [
        'Argentina',
        'Bolivia',
        'Brazil',
        'Chile',
        'Colombia',
        'Costa Rica',
        'Cuba',
        'Dominican Republic',
        'Ecuador',
        'El Salvador',
        'French Guiana',
        'Guadeloupe',
        'Guatemala',
        'Haiti',
        'Honduras',
        'Martinique',
        'Mexico',
        'Nicaragua',
        'Panama',
        'Paraguay',
        'Peru',
        'Puerto Rico',
        'Saint Barthélemy',
        'Saint Martin',
        'Uruguay',
        'Venezuela'
    ]:
        models.Country.objects.create(name=name)


def insert_data_literary_genre(apps, schema_editor):
    """
    Inserts default data into the LiteraryGenre model
    """

    for name in [
        'testimonial writing',
        'survival poetry'
    ]:
        models.LiteraryGenre.objects.create(name=name)


def insert_data_social_media_platform(apps, schema_editor):
    """
    Inserts default data into the SocialMediaPlatform model
    """

    for obj in [
        {
            'name': 'X (formerly Twitter)',
            'url': 'https://www.twitter.com'
        },
        {
            'name': 'Facebook',
            'url': 'https://www.facebook.com'
        },
        {
            'name': 'Instagram',
            'url': 'https://www.instagram.com'
        },
        {
            'name': 'LinkedIn',
            'url': 'https://www.linkedin.com'
        },
        {
            'name': 'YouTube',
            'url': 'https://www.youtube.com'
        },
        {
            'name': 'WhatsApp',
            'url': 'https://www.whatsapp.com'
        }
    ]:
        models.SocialMediaPlatform.objects.create(**obj)


class Migration(migrations.Migration):

    dependencies = [
        ('researchdata', '0001_initial')
    ]

    operations = [
        migrations.RunPython(insert_data_country),
        migrations.RunPython(insert_data_literary_genre),
        migrations.RunPython(insert_data_social_media_platform)
    ]
