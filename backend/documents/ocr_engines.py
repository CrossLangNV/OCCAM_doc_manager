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
            # Always have a description to guide the user.
            description = str(engine_info)

        # Check if LayoutAnalysisModel already exist:
        LayoutAnalysisModel.objects.update_or_create(name=engine_name,
                                                     defaults={'description': description,
                                                               'config': engine_info
                                                               }
                                                     )

    return


def get_PERO_OCR_engine_id(ocr_engine: LayoutAnalysisModel):
    if ocr_engine.config.get(KEY_LINK) != PERO_OCR_ENGINE:
        warnings.warn("Expected conformation that this is a PERO-OCR engine.", UserWarning)

    pero_engine_id = ocr_engine.config[KEY_ENGINE_ID]
    return pero_engine_id
