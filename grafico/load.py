from typing import Mapping, Any, Iterable

from dataclasses import dataclass


JSON = Mapping[str, dict]


@dataclass
class Entity:
    entity_type: str
    document_id: str
    properties: Mapping[str, Any]

    @classmethod
    def from_json(cls, file_name: str, metadata: JSON) -> Iterable['Entity']:
        entity_type = cls._entity_type(file_name)
        content_key = next((k for k in metadata if k.startswith(entity_type)))
        return (cls(
            entity_type=entity_type,
            document_id=cls._document_id(entity_content),
            properties=cls._properties(entity_content)
        ) for entity_content in metadata[content_key])

    @classmethod
    def _entity_type(cls, file_name) -> str:
        suffix = '.json'
        assert file_name.endswith(suffix)
        return file_name[:-len(suffix)]

    @classmethod
    def _document_id(cls, metadata) -> str:
        return metadata['hca_ingest']['document_id']

    @classmethod
    def _properties(cls, content: Mapping[str, Any]) -> Mapping[str, Any]:
        properties = {}
        for k, v in content['content'].items():
            if type(v) == dict:
                # TODO: too hard... figure out later
                pass
            elif type(v) == list:
                # TODO: ditto
                pass
            else:
                assert type(v) in (str, int, float, bool)
                properties[k] = v
        return properties


def extract_json(json: JSON) -> Iterable[Entity]:
    for file_name, metadata in json.items():
        if file_name not in ('links.json', 'project.json'):
            for entity in Entity.from_json(file_name, metadata):
                yield entity
        else:
            pass
