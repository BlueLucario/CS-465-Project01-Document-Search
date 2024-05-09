from typing import List
from inverted_index import getInvertedIndex
from document import AbstractDocument

def get_document_content(id: str) -> List[AbstractDocument]: # Hacky: Assumes a lot
    invertedIndex = getInvertedIndex()
    assert hasattr(invertedIndex, 'documents')
    
    for document in invertedIndex.documents:
        if str(document.id) == id:
            assert hasattr(document, 'data')
            return document.data 
        
    raise RuntimeError(f'Document with id {id} not found')