from django.db import migrations
from researchdata import models


def insert_data_country(apps, schema_editor):
    """
    Inserts default data into the Country model
    """

    for country in [
        { 'name': 'Argentina', 'longitude': '-58.381592', 'latitude': '-34.603722' },
        { 'name': 'Bolivia', 'longitude': '	-68.119293', 'latitude': '-16.489689' },
        { 'name': 'Chile', 'longitude': '-70.645348', 'latitude': '-33.459229' },
        { 'name': 'Colombia', 'longitude': '-74.063644', 'latitude': '4.624335' },
        { 'name': 'Costa Rica', 'longitude': '-84.087502', 'latitude': '9.934739' },
        { 'name': 'Cuba', 'longitude': '-82.366592', 'latitude': '23.113592' },
        { 'name': 'Dominican Republic', 'longitude': '-69.929611', 'latitude': '18.483402' },
        { 'name': 'Ecuador', 'longitude': '-78.467834', 'latitude': '-0.180653' },
        { 'name': 'El Salvador', 'longitude': '-88.8965', 'latitude': '13.7942' },
        { 'name': 'Guatemala', 'longitude': '-90.522713', 'latitude': '14.628434' },
        { 'name': 'Honduras', 'longitude': '-87.202438', 'latitude': '14.081999' },
        { 'name': 'Mexico', 'longitude': '-99.133209', 'latitude': '19.432608' },
        { 'name': 'Nicaragua', 'longitude': '-86.251389', 'latitude': '12.136389' },
        { 'name': 'Panama', 'longitude': '-80.7821', 'latitude': '8.5380' },
        { 'name': 'Paraguay', 'longitude': '-58.4438', 'latitude': '-23.4425' },
        { 'name': 'Peru', 'longitude': '-75.015152', 'latitude': '-9.189967' },
        { 'name': 'Puerto Rico', 'longitude': '-66.664513', 'latitude': '18.200178' },
        { 'name': 'Uruguay', 'longitude': '-56.164532', 'latitude': '-34.901112' },
        { 'name': 'Venezuela', 'longitude': '-66.916664', 'latitude': '10.500000' },
        { 'name': 'Morocco', 'longitude': '-7.0926', 'latitude': '31.7917' },
    ]:
        models.Country.objects.filter(name=country['name']).update(
            longitude=country['longitude'],
            latitude=country['latitude']
        )


class Migration(migrations.Migration):

    dependencies = [
        ('researchdata', '0003_alter_socialmediaplatform_options_and_more')
    ]

    operations = [
        migrations.RunPython(insert_data_country),
    ]
