from typing import Dict, Any, Optional

class Document:
    def __init__(
        self,
        document_id: str,
        title: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        self.document_id = document_id
        self.title = title
        self.data = data or {}

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'document_id': self.document_id
        }
        if self.title:
            result['title'] = self.title
        if self.data:
            result.update(self.data)
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        document_id = data.get('dc:identifier', '').split(':')[-1] if 'dc:identifier' in data else data.get('document_id', '')
        return cls(
            document_id=document_id,
            title=data.get('dc:title', ''),
            data=data
        )

