from typing import Dict, Any, Optional

class Author:
    def __init__(
        self,
        author_id: str,
        name: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        self.author_id = author_id
        self.name = name
        self.data = data or {}

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'author_id': self.author_id
        }
        if self.name:
            result['name'] = self.name
        if self.data:
            result.update(self.data)
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Author':
        author_id = data.get('author_id') or data.get('dc:identifier', '').split(':')[-1]
        return cls(
            author_id=author_id,
            name=data.get('name') or data.get('preferred-name', {}).get('surname', ''),
            data=data
        )

