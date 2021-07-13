import os

from django.contrib.auth.models import User
from rest_framework.test import APIClient

from documents.models import Document, Page, Overlay

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
URL_PAGE = "/documents/api/pages"
URL_OVERLAYS = "/documents/api/overlays"

if 0:
    FILENAME_XML = os.path.join(ROOT, "backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml")
else:
    FILENAME_XML = os.path.join(ROOT, "backend/tests/examples_data/page_minimal_working_example.xml")
FILENAME_IMAGE = os.path.join(ROOT, "backend/tests/examples_data/19154766-page0.jpg")


def login(self=None):
    """

    Args:
        self: Test class object to save self.username and self.password to.

    Returns:

    """
    username = 'testuser@test.com',
    password = "Dummy@123"

    if self is not None:
        self.username = username
        self.password = password

    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()

    client = APIClient()
    client.force_authenticate(user=user)

    return client, user


def create(client=None,
           user: User = None,
           ):
    doc = Document.objects.create(name="Declaration of Independence",
                                  content="Stolen by Nicolas Cage.",
                                  user=user)

    page = Page.objects.create(
        # filename=name,
        # path=path,
        document=doc
    )
    with open(FILENAME_IMAGE, "rb") as f:
        page.update_image(f)

    o1 = Overlay.objects.create(page=page, source_lang="NL")
    with open(FILENAME_XML, "rb") as f:
        o1.update_xml(f)

    if client is None:
        # You might have to send the client with it
        client, user = login()

    with open(FILENAME_IMAGE, "rb") as f:
        response = client.post(URL_PAGE, data={"document": doc.id,
                                               "file": f,
                                               },
                               format="multipart",
                               )

    with open(FILENAME_XML, "r") as f:
        response = client.post(URL_PAGE, data={"document": doc.id,
                                               "file": f
                                               },
                               format="multipart"
                               )

    with open(FILENAME_XML, "r") as f:
        response = client.post(URL_OVERLAYS, data={"page": page.id, "file": f},
                               format="multipart")

    return
