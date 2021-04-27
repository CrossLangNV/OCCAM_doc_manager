import json
import os
from typing import Tuple, List

from lxml import etree

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Coords:
    def __init__(self, w0: float, h0: float, w1: float, h1: float,
                 l_co: List[Tuple[float]]=None):
        self.w0 = float(w0)
        self.h0 = float(h0)
        self.w1 = float(w1)
        self.h1 = float(h1)

        self.l_co = list(map(lambda a: tuple(map(float, a)), l_co))

    @classmethod
    def from_text_region_lxml(cls, element, xmlns):
        coords = _get_unique_lxml_child(element, './/{%s}Coords' % xmlns)

        s_l_co = coords.attrib.get('points')

        l_co = [tuple(map(float, s_co_i.split(','))) for s_co_i in s_l_co.strip().replace('  ', ' ').split(' ')]

        w = list(map(lambda xy: xy[0], l_co))
        h = list(map(lambda xy: xy[1], l_co))

        w0 = min(w)
        h0 = min(h)
        w1 = max(w)
        h1 = max(h)

        return cls(w0, h0, w1, h1, l_co = l_co)


def get_text_from_text_region_lxml(element, xmlns):
    path = './/{{{xmlns}}}TextEquiv/{{{xmlns}}}Unicode'.format(xmlns=xmlns)

    unicode = _get_unique_lxml_child(element, path)
    unicode_text = unicode.text
    return unicode_text.strip() if unicode_text else ''


def _get_unique_lxml_child(element, path):
    a = list(element.iterfind(path))

    assert len(a) == 1, f'Should only find one {path} element: {a}'

    b = a[0]

    return b


def lxml_text_region_iterator(filename):
    parser = etree.XMLParser(remove_blank_text=True)
    element_tree = etree.parse(filename,
                               parser)

    namespace = {'page-1': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15',
                 }

    xmlns = element_tree.getroot().tag.split('}')[0].strip('{')

    if xmlns in namespace.values():

        # l_text_page = []

        for region in element_tree.iterfind('.//{%s}TextRegion' % xmlns):
            # region

            l_text_line_paragraph = []

            for textline in region.iterfind(
                './/{{{xmlns}}}TextLine'.format(xmlns=xmlns)
            ):
                co = Coords.from_text_region_lxml(textline, xmlns)

                text_textline = get_text_from_text_region_lxml(textline, xmlns)

                yield co, text_textline


def main(filename, b_rectangle=False):
    l = lxml_text_region_iterator(filename)

    d = {"type": "FeatureCollection",
         'features': []}

    for co, text_textline in l:


        if b_rectangle:

            h0, w0, h1, w1 = co.h0, co.w0, co.h1, co.w1

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Rectangle",
                    "coordinates": [h0, w0, h1, w1]
                },
                "properties": {
                    "name": text_textline
                }
            }
        else:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [(h, w) for (w, h) in co.l_co]
                },
                "properties": {
                    "name": text_textline
                }
            }

        d.get('features').append(feature)

    return d


if __name__ == '__main__':
    if 0:
        FILENAME = os.path.join(ROOT, 'src/assets/data/KB_JB840_1919-04-01_01_0_fixed.xml')
    else:
        FILENAME = os.path.join(ROOT, 'src/assets/data/KB_JB840_1919-04-01_01_0_fixed_NL_EN.xml')

    main(FILENAME)