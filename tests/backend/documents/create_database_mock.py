from documents.models import Document, Image


def create():
    doc = Document.objects.create(
        name='Declaration of Independence',
        content='Stolen by Nicolas Cage.'
    )
    name = 'a test image'
    path = 'a/b/c.def'
    width = 10
    height = 20

    Image.objects.create(
        filename=name,
        path=path,
        width=width,
        height=height,
        document=doc
    )
