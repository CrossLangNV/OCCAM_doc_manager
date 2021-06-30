from documents.models import LayoutAnalysisModel
from documents.ocr_connector import get_engines, KEY_DESCRIPTION

KEY_LINK = 'link'
PERO_OCR_ENGINE = 'https://pero-ocr.fit.vutbr.cz/'


def init_engines() -> None:
    """
    This will initialise the LayoutAnalysisModel models with the available engines,
    according to the ones available by PERO-OCR.

    Returns:

    """

    # TODO get from config files.
    # TODO make a user-script that builds these config files.

    for engine_name, engine_info in get_engines().items():

        engine_info[KEY_LINK] = PERO_OCR_ENGINE

        description = engine_info.get(KEY_DESCRIPTION)
        if description is None:
            # Always have a description to guide the user.
            description = str(engine_info)

        # Check if LayoutAnalysisModel already exist:
        LayoutAnalysisModel.objects.update_or_create(name=engine_name,
                                                     defaults={'description': description,
                                                               'config': engine_info
                                                               }
                                                     )

    return
