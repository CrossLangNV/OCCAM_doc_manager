import mimetypes
from datetime import date

from documents.models import Page
from . import metadata


class MetadataDjango(metadata.Metadata):
    @classmethod
    def from_page(cls, page: Page):
        """
        Will not add the source language if it isn't recognised yet.

        page: Page object or id of page.
        """

        if isinstance(page, str):
            page = Page.objects.get(pk=page)

        page_name = page.file.name

        def _get_source(page):
            try:
                source = page.page_overlay.all()[0].source_lang
            except Exception as err:
                # 'No source language found.'
                return None
            else:
                return source

        source = _get_source(page)
        document_name = page.document.name
        today = date.today()
        content_type_file = mimetypes.guess_type(page.file.file.name)[0]

        return cls(titles=f'Page {page_name}',
                   subjects='Pages',
                   descriptions=f'Page processed by OCCAM.',
                   dates=today.strftime("%Y-%m-%d"),
                   types=["image", "text", "XML"],
                   formats=[content_type_file, "text/plain", 'application/xml'],
                   sources=f"The Document '{document_name}'",
                   languages=source
                   )
