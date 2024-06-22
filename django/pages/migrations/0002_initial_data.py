from django.db import migrations
from pages import models


def create_pages(apps, schema_editor):
    """
    Create Page objects with HTML content
    """

    # Welcome
    content = """

<h3>Welcome</h3>
<p>
    Coming soon...
</p>

""".strip()
    models.Page.objects.create(
        name='Welcome',
        content_en=content,
        content_es=content,
        published=True
    )

    # About
    content = """

<h2>About</h2>
<p>
    Coming soon...
</p>

""".strip()
    models.Page.objects.create(
        name='About',
        content_en=content,
        content_es=content,
        published=True
    )

    # Team Members
    content = """

<h2>Team Members</h2>
<p>
    Coming soon...
</p>

""".strip()
    models.Page.objects.create(
        name='Team Members',
        content_en=content,
        content_es=content,
        published=True
    )

    # Publications
    content = """

<h2>Publications</h2>
<p>
    Coming soon...
</p>

""".strip()
    models.Page.objects.create(
        name='Publications',
        content_en=content,
        content_es=content,
        published=True
    )

        # Contact Us
    content = """

<h2>Contact Us</h2>
<p>
    Coming soon...
</p>

""".strip()
    models.Page.objects.create(
        name='Contact Us',
        content_en=content,
        content_es=content,
        published=True
    )

    # More Resources
    content = """

<h2>More Resources</h2>
<p>
    Coming soon...
</p>

""".strip()
    models.Page.objects.create(
        name='More Resources',
        content_en=content,
        content_es=content,
        published=True
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_pages),
    ]
