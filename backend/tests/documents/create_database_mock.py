import os

from django.contrib.auth.models import User
from django.test import Client

from documents.models import Document, Page, Overlay

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
URL_PAGE = '/documents/api/pages/'

if 0:
    FILENAME_XML = os.path.join(ROOT, 'backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml')
else:
    FILENAME_XML = os.path.join(ROOT, 'backend/tests/examples_data/page_minimal_working_example.xml')
FILENAME_IMAGE = os.path.join(ROOT, 'backend/tests/examples_data/19154766-page0.jpg')


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
    with open(FILENAME_IMAGE, 'rb') as f:
        page.update_image(f)

    o1 = Overlay.objects.create(
        page=page
    )
    with open(FILENAME_XML, 'rb') as f:
        o1.update_xml(f)

    if client is None:
        # You might have to send the client with it
        client, _ = login()

    with open(FILENAME_IMAGE, 'rb') as f:
        files = {'file': f}
        response = client.post(URL_PAGE,
                               data={
                                   'document': doc.id,
                                   'file': f
                               },
                               files=files)

    with open(FILENAME_XML, 'rb') as f:
        files = {'file': f}
        response = client.post(URL_PAGE,
                               data={
                                   'document': doc.id,
                                   'file': f
                               },
                               files=files)

    # URL = '/documents/api/overlays/'
    URL = '/documents/overlays/'
    with open(FILENAME_XML, 'r') as f:
        files = {'file': f}
        response = client.post(URL,
                               data={
                                   'page': page.id,
                                   'file': f
                               },
                               files=files)
