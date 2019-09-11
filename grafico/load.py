from typing import Mapping, Any, Iterable

from dataclasses import dataclass


JSON = Mapping[str, dict]


@dataclass
class Entity:
    entity_type: str
    document_id: str
    properties: Mapping[str, Any]


class Transformer:

    def extract_json(self, json: JSON) -> Iterable[Entity]:
        for file_name, metadata in json.items():
            if file_name not in ('links.json', 'project.json'):
                for entity in self.from_json(file_name, metadata):
                    yield entity
            else:
                pass

    def from_json(self, file_name: str, metadata: JSON) -> Iterable['Entity']:
        entity_type = self._entity_type(file_name)
        content_key = next((k for k in metadata if k.startswith(entity_type)))
        return (Entity(
            entity_type=entity_type,
            document_id=self._document_id(entity_content),
            properties=self._properties(entity_content)
        ) for entity_content in metadata[content_key])

    def _entity_type(self, file_name) -> str:
        suffix = '.json'
        assert file_name.endswith(suffix)
        return file_name[:-len(suffix)]

    def _document_id(self, metadata) -> str:
        return metadata['hca_ingest']['document_id']

    def _properties(self, content: Mapping[str, Any]) -> Mapping[str, Any]:
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
