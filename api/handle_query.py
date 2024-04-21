from typing import List
from inverted_index import getInvertedIndex
from document import AbstractDocument

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
    while True:
        query = input('Enter query: ')

        matchedDocuments = handle_query(query)

        print(f'Matched documents for query {query}: {matchedDocuments}')