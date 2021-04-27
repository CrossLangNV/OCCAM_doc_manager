import os

from django.contrib.auth.models import User
from django.test import Client

from documents.models import Document, Page, Overlay

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))


def login(self=None):
    username = 'dummy@gmail.com'
    password = 'Dummy@123'

    if self is not None:
        self.username = username
        self.password = password

    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()

    # initialize the APIClient app
    client = Client()
    b = client.login(username=username, password=password)
    assert b
    return client, user


def create(client=None):
    doc = Document.objects.create(
        name='Declaration of Independence',
        content='Stolen by Nicolas Cage.'
    )
    name = 'a test image'
    path = 'a/b/c.def'
    width = 10
    height = 20

    page = Page.objects.create(
        # filename=name,
        # path=path,
        width=width,
        height=height,
        document=doc
    )

    o1 = Overlay.objects.create(
        page=page
    )

    if client is None:
        # You might have to send the client with it
        client, _ = login()

    URL_PAGE = '/documents/api/pages'
    filename_image = os.path.join(ROOT, 'backend/tests/examples_data/19154766-page0.jpg')
    with open(filename_image, 'rb') as f:
        files = {'file': f}
        response = client.post(URL_PAGE,
                               data={
                                   'document': doc.id,
                                   'file': f
                               },
                               files=files)

    filename_xml = os.path.join(ROOT, 'backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml')
    with open(filename_xml, 'rb') as f:
        files = {'file': f}
        response = client.post(URL_PAGE,
                               data={
                                   'document': doc.id,
                                   'file': f
                               },
                               files=files)

    # URL = '/documents/api/overlays/'
    URL = '/documents/overlays/'
    with open(filename_xml, 'r') as f:
        files = {'file': f}
        response = client.post(URL,
                               data={
                                   'page': page.id,
                                   'file': f
                               },
                               files=files)
