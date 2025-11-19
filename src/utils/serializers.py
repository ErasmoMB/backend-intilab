from bson import ObjectId
from typing import Dict, Any

def serialize_id(doc: Dict[str, Any]) -> Dict[str, Any]:
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc

