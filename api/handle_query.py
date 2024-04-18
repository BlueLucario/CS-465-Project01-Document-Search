from abc import ABC, abstractmethod
from typing import List
from inverted_index import AbstractInvertedIndex, SimpleInvertedIndex
from document import AbstractDocument
    
def getInvertedIndex() -> AbstractInvertedIndex:
    invertedIndex = SimpleInvertedIndex()
    while True:
        yield invertedIndex

def handle_query(query: str) -> List[AbstractDocument]:
    invertedIndex = getInvertedIndex()
    return invertedIndex.handleQuery(query)

if __name__ == '__main__':
    '''
    1. Create the inverted index
    2. Receive the query
    3. Retrieve appropriate documents
    4. Return document names
    '''    
    query = input('Enter query: ')

    matchedDocuments = handle_query(query)

    print(f'Matched documents for query {query}: {matchedDocuments}')