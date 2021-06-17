from datetime import date

from documents.models import Page
from . import metadata


class MetadataDjango(metadata.Metadata):
    @classmethod
    def from_page(cls, page: Page):
        """
        page: Page object or id of page.
        """

        if isinstance(page, str):
            page = Page.objects.get(pk=page)

        page_name = page.file.name
        source = page.page_overlay.all()[0].source_lang

        document_name = page.document.name

        today = date.today()

        return cls(titles=f'Page {page_name}',
                   subject='Pages',
                   descriptions=f'Page processed by OCCAM.',
                   dates=today.strftime("%Y-%m-%d"),
                   types=["image", "text", "XML"],
                   # TODO get extension
                   formats=["image/png", "/txt", 'application/xml'],
                   sources=f"The Document '{document_name}'",
                   languages=source
                   )
