import os

from django.core.files import File

from documents.models import Document, Page, Overlay

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))


def create():
    doc = Document.objects.create(
        name='Declaration of Independence',
        content='Stolen by Nicolas Cage.'
    )
    name = 'a test image'
    path = 'a/b/c.def'
    width = 10
    height = 20

    page = Page.objects.create(
        filename=name,
        path=path,
        width=width,
        height=height,
        document=doc
    )

    Overlay.objects.create(
        page=page
    )

    filename_xml = os.path.join(ROOT, 'backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml')
    with File(f := open(filename_xml, 'r')) as django_file:
        Overlay.objects.create(
            page=page,
            xml=django_file
        )
