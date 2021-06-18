from typing import Union

from dcxml import simpledc

OCCAM = 'OCCAM'


class Metadata:
    """
    Metadata class
    """

    def __init__(self,
                 titles: Union[list, str] = [],
                 creators: Union[list, str] = [OCCAM],
                 subjects: Union[list, str] = [],
                 descriptions: Union[list, str] = [],
                 publishers: Union[list, str] = [OCCAM],
                 contributors: Union[list, str] = [OCCAM],
                 dates: Union[list, str] = [],
                 types: Union[list, str] = [],
                 formats: Union[list, str] = [],
                 identifiers: Union[list, str] = [],
                 sources: Union[list, str] = [],
                 languages: Union[list, str] = [],
                 relations: Union[list, str] = [],
                 coverage: Union[list, str] = [],
                 rights: Union[list, str] = [],
                 ):
        """
        Elements for the Dublin Core metadata format. Every element can occur multiple times.
        https://www.dublincore.org/specifications/dublin-core/usageguide/2001-04-12/generic/

        Args:
            titles (list[str]): Title, e.g. "A Pilot's Guide to Aircraft Insurance"
            creators (list[str]): Author/Creator, e.g. "Duncan, Phyllis-Anne"
            subjects (list[str]): Subject and Keywords, e.g. "Dogs"
            descriptions (list[str]): Description, e.g. "Illustrated guide to airport markings and lighting signals, with particular reference to SMGCS (Surface Movement Guidance and Control System) for airports with low visibility conditions"
            publishers (list[str]): Publisher, e.g. "University of Miami. Dept. of Economics"
            contributors (list[str]): Other Contributor. By default OCCAM
            dates (list[str]): Date, e.g. "1998-02-16"
            types (list[str]): Resource Type, e.g. Multimedia educational program with interactive assignments:
                Type="text"
                Type="image"
                Type="software"
                Type="interactive"
            formats (list[str]): Format, e.g. "image/gif 640 x 512 pixels"
            identifiers (list[str]): Resource Identifier, e.g. "0385424728" [ISBN]
            sources (list[str]): Source, e.g. "RC607.A26W574 1996">
                [where "RC607.A26W574 1996" is the call number of the print version of the resource, from which the present version was scanned]
            languages (list[str]): Language, e.g. "en;fr"
            relations (list[str]): Relation, e.g. "IsReferencedBy Engels' Origin of the Family, Private Property and the State"
            coverage (list[str]): Coverage, e.g. ["1995-1996", "Upstate New York"]
            rights (list[str]): Rights Management, e.g. "http://cs-tr.cs.cornell.edu/Dienst/Repository/2.0/Terms"
        """

        self.titles = self._single_to_list(titles)
        self.creators = self._single_to_list(creators)
        self.subjects = self._single_to_list(subjects)
        self.descriptions = self._single_to_list(descriptions)
        self.publishers = self._single_to_list(publishers)
        self.contributors = self._single_to_list(contributors)
        self.dates = self._single_to_list(dates)
        self.types = self._single_to_list(types)
        self.formats = self._single_to_list(formats)
        self.identifiers = self._single_to_list(identifiers)
        self.sources = self._single_to_list(sources)
        self.languages = self._single_to_list(languages)
        self.relations = self._single_to_list(relations)
        self.coverage = self._single_to_list(coverage)
        self.rights = self._single_to_list(rights)

    def get_dict(self):
        data = dict(
            titles=self.titles,
            creators=self.creators,
            subjects=self.subjects,
            descriptions=self.descriptions,
            publishers=self.publishers,
            contributors=self.contributors,
            dates=self.dates,
            types=self.types,
            formats=self.formats,
            identifiers=self.identifiers,
            sources=self.sources,
            languages=self.languages,
            relations=self.relations,
            coverage=self.coverage,
            rights=self.rights,
        )

        # Remove empty elements
        data = {key: value for key, value in data.items() if value}  # No list items

        return data

    def to_xml(self):
        """
        According to Dublin Core
        https://www.dublincore.org/specifications/dublin-core/

        data = dict(
            contributors=['CERN'],
            coverage=['Geneva'],
            creators=['CERN'],
            dates=['2002'],
            descriptions=['Simple Dublin Core generation'],
            formats=['application/xml'],
            identifiers=['dublin-core'],
            languages=['en'],
            publishers=['CERN'],
            relations=['Invenio Software'],
            rights=['GPLv2'],
            sources=['Python'],
            subjects=['XML'],
            titles=['Dublin Core XML'],
            types=['Software'],
        )
        """

        data = self.get_dict()
        etree = simpledc.dump_etree(data)
        xml = simpledc.etree_to_string(etree)

        return xml

    @staticmethod
    def _single_to_list(el):
        """ Can convert a single element to a list.

        Args:
            el:

        Returns:

        """

        return [el] if isinstance(el, str) else el

    def __str__(self):
        return self.to_xml()
