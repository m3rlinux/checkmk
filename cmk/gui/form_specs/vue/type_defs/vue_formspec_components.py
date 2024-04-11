# generated by datamodel-codegen:
#   filename:  vue_formspec_components.json
#   timestamp: 2024-05-23T12:11:53+00:00

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from cmk.gui.form_specs.vue.type_defs.vue_validators import VueValidators


@dataclass
class VueBase:
    title: str
    help: str
    validators: list[VueValidators] = field(default_factory=list)


@dataclass
class VueInteger(VueBase):
    vue_type: str = "integer"
    label: Optional[str] = None
    unit: Optional[str] = None


@dataclass
class VueFloat(VueBase):
    vue_type: str = "float"
    label: Optional[str] = None
    unit: Optional[str] = None


@dataclass
class VueLegacyValuespec(VueBase):
    vue_type: str = "legacy_valuespec"


@dataclass
class VueText(VueBase):
    vue_type: str = "text"
    placeholder: Optional[str] = None


@dataclass
class Model:
    all_schemas: Optional[List[VueSchema]] = None


@dataclass
class VueList(VueBase):
    vue_type: str = "list"
    add_text: Optional[str] = None
    vue_schema: Optional[VueSchema] = None


@dataclass
class VueDictionaryElement:
    ident: str
    required: bool
    default_value: Any
    vue_schema: VueSchema


@dataclass
class VueDictionary(VueBase):
    elements: List[VueDictionaryElement] = field(default_factory=list)
    vue_type: str = "dictionary"


VueSchema = Union[VueInteger, VueFloat, VueText, VueDictionary, VueList, VueLegacyValuespec]
