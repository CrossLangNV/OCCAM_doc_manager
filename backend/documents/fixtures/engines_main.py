"""
Script to build engines.json based on the PERO-OCR app.
"""

import json
import os
import warnings

from documents.models import LayoutAnalysisModel
from documents.ocr_engines import init_engines

DIR_FIXTURES = os.path.abspath(os.path.join(os.path.dirname(__file__)))
ENGINES_JSON = os.path.join(DIR_FIXTURES, 'engines.json')

if not os.path.exists(ENGINES_JSON):
    warnings.warn(f"Can't find file: {ENGINES_JSON}", UserWarning)


def main():
    init_engines()

    model = f"{LayoutAnalysisModel.__module__.split('.', 1)[0]}." \
            f"{LayoutAnalysisModel.__name__.lower()}"

    engines = LayoutAnalysisModel.objects.all()
    json_engines = []

    for engine in engines:
        json_engines.append({
            "model": model,
            "pk": engine.pk,
            "fields": {
                LayoutAnalysisModel.name.field.name: engine.name,
                LayoutAnalysisModel.description.field.name: engine.description,
                LayoutAnalysisModel.config.field.name: engine.config,
            }
        })

    with open(ENGINES_JSON, 'w') as outfile:
        json.dump(json_engines, outfile,
                  indent=2)

    return


if __name__ == '__main__':
    main()
