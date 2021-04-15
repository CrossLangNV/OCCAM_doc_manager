from documents.models import Document, Page


def create():
    doc = Document.objects.create(
        name='Declaration of Independence',
        content='Stolen by Nicolas Cage.'
    )
    name = 'a test image'
    path = 'a/b/c.def'
    width = 10
    height = 20

    Page.objects.create(
        filename=name,
        path=path,
        width=width,
        height=height,
        document=doc
    )
