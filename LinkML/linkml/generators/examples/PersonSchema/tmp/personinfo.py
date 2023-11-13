# Auto generated from personinfo.yaml by pythongen.py version: 0.0.1
# Generation date: 2023-10-19T21:23:46
# Schema: personinfo
#
# id: https://w3id.org/linkml/examples/personinfo
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PERSONINFO = CurieNamespace('personinfo', 'https://w3id.org/linkml/examples/personinfo')
DEFAULT_ = PERSONINFO


# Types

# Class references



@dataclass
class Person(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Person
    class_class_curie: ClassVar[str] = "personinfo:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Person

    contactinfo: str = None
    achternaam: Optional[str] = None
    alternatieveNaam: Optional[str] = None
    geboortenaam: Optional[str] = None
    gebruikteVoornaam: Optional[str] = None
    geslacht: Optional[str] = None
    patroniem: Optional[str] = None
    volledigeNaam: Optional[str] = None
    voornaam: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.contactinfo):
            self.MissingRequiredField("contactinfo")
        if not isinstance(self.contactinfo, str):
            self.contactinfo = str(self.contactinfo)

        if self.achternaam is not None and not isinstance(self.achternaam, str):
            self.achternaam = str(self.achternaam)

        if self.alternatieveNaam is not None and not isinstance(self.alternatieveNaam, str):
            self.alternatieveNaam = str(self.alternatieveNaam)

        if self.geboortenaam is not None and not isinstance(self.geboortenaam, str):
            self.geboortenaam = str(self.geboortenaam)

        if self.gebruikteVoornaam is not None and not isinstance(self.gebruikteVoornaam, str):
            self.gebruikteVoornaam = str(self.gebruikteVoornaam)

        if self.geslacht is not None and not isinstance(self.geslacht, str):
            self.geslacht = str(self.geslacht)

        if self.patroniem is not None and not isinstance(self.patroniem, str):
            self.patroniem = str(self.patroniem)

        if self.volledigeNaam is not None and not isinstance(self.volledigeNaam, str):
            self.volledigeNaam = str(self.volledigeNaam)

        if self.voornaam is not None and not isinstance(self.voornaam, str):
            self.voornaam = str(self.voornaam)

        super().__post_init__(**kwargs)


@dataclass
class Nationaliteit(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Nationaliteit
    class_class_curie: ClassVar[str] = "personinfo:Nationaliteit"
    class_name: ClassVar[str] = "Nationaliteit"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Nationaliteit

    nationaliteit: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.nationaliteit is not None and not isinstance(self.nationaliteit, str):
            self.nationaliteit = str(self.nationaliteit)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.achternaam = Slot(uri=PERSONINFO.achternaam, name="achternaam", curie=PERSONINFO.curie('achternaam'),
                   model_uri=PERSONINFO.achternaam, domain=None, range=Optional[str])

slots.alternatieveNaam = Slot(uri=PERSONINFO.alternatieveNaam, name="alternatieveNaam", curie=PERSONINFO.curie('alternatieveNaam'),
                   model_uri=PERSONINFO.alternatieveNaam, domain=None, range=Optional[str])

slots.contactinfo = Slot(uri=PERSONINFO.contactinfo, name="contactinfo", curie=PERSONINFO.curie('contactinfo'),
                   model_uri=PERSONINFO.contactinfo, domain=None, range=str)

slots.geboortenaam = Slot(uri=PERSONINFO.geboortenaam, name="geboortenaam", curie=PERSONINFO.curie('geboortenaam'),
                   model_uri=PERSONINFO.geboortenaam, domain=None, range=Optional[str])

slots.gebruikteVoornaam = Slot(uri=PERSONINFO.gebruikteVoornaam, name="gebruikteVoornaam", curie=PERSONINFO.curie('gebruikteVoornaam'),
                   model_uri=PERSONINFO.gebruikteVoornaam, domain=None, range=Optional[str])

slots.geslacht = Slot(uri=PERSONINFO.geslacht, name="geslacht", curie=PERSONINFO.curie('geslacht'),
                   model_uri=PERSONINFO.geslacht, domain=None, range=Optional[str])

slots.patroniem = Slot(uri=PERSONINFO.patroniem, name="patroniem", curie=PERSONINFO.curie('patroniem'),
                   model_uri=PERSONINFO.patroniem, domain=None, range=Optional[str])

slots.volledigeNaam = Slot(uri=PERSONINFO.volledigeNaam, name="volledigeNaam", curie=PERSONINFO.curie('volledigeNaam'),
                   model_uri=PERSONINFO.volledigeNaam, domain=None, range=Optional[str])

slots.voornaam = Slot(uri=PERSONINFO.voornaam, name="voornaam", curie=PERSONINFO.curie('voornaam'),
                   model_uri=PERSONINFO.voornaam, domain=None, range=Optional[str])

slots.nationaliteit = Slot(uri=PERSONINFO.nationaliteit, name="nationaliteit", curie=PERSONINFO.curie('nationaliteit'),
                   model_uri=PERSONINFO.nationaliteit, domain=None, range=Optional[str])