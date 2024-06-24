# Generated by Django 4.2.13 on 2024-06-04 09:55

from django.db import migrations, models
import pages.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(help_text='\n        Ensure the name of the file you upload is unique and descriptive.\n        <br>Look at existing uploaded files to see the recommended naming convention.\n        ', upload_to=pages.models.FileUpload.get_upload_to),
        ),
    ]
