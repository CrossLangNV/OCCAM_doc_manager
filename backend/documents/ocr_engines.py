import warnings

from documents.models import LayoutAnalysisModel
from documents.ocr_connector import get_engines, KEY_DESCRIPTION, KEY_ENGINE_ID

KEY_LINK = 'link'
PERO_OCR_ENGINE = 'https://pero-ocr.fit.vutbr.cz/'


def init_engines() -> None:
    """
    This will initialise the LayoutAnalysisModel models with the available engines,
    according to the ones available by PERO-OCR.

    Returns:

    """

    LayoutAnalysisModel.objects.update_or_create(name='No OCR',
                                                 defaults={'description': 'Skip OCR and upload your own transcription.',
                                                           'config': {}
                                                           }
                                                 )

    for engine_name, engine_info in get_engines().items():
        engine_info[KEY_LINK] = PERO_OCR_ENGINE

        description = engine_info.get(KEY_DESCRIPTION)

        if description is None:
            # Would be nice to always have a description to guide the user.
            # e.g. str(engine_info)
            description = ''

        # Check if LayoutAnalysisModel already exist:
        LayoutAnalysisModel.objects.update_or_create(name=_nice_string(engine_name),
                                                     defaults={'description': _nice_string(description),
                                                               'config': engine_info
                                                               }
                                                     )

    return


def get_PERO_OCR_engine_id(ocr_engine: LayoutAnalysisModel):
    if ocr_engine.config.get(KEY_LINK) != PERO_OCR_ENGINE:
        warnings.warn("Expected conformation that this is a PERO-OCR engine.", UserWarning)

    pero_engine_id = ocr_engine.config[KEY_ENGINE_ID]
    return pero_engine_id


def _nice_string(engine_name: str):
    """
    Cleanup a sentence by
    * removing underscores
    * Capitalizing the first letter.

    Args:
        engine_name:

    Returns:

    """

    engine_name = engine_name.replace('_', ' ')

    # Only make sure that the first character of the string is in upper case
    engine_name = engine_name[:1].upper() + engine_name[1:]

    return engine_name
