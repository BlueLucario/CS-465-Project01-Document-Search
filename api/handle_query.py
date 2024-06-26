 # handle_query.py (python)
 # Will Moss & Benjamin Weeg (Group 1)
 # Started: 
 # Last edited: 2024-05-09 (yyyy mm dd)

from typing import List
from inverted_index import getInvertedIndex
from document import AbstractDocument

def handle_query(query: str) -> List[AbstractDocument]:
    invertedIndex = getInvertedIndex()
    return invertedIndex.handleQuery(query)

if __name__ == '__main__':
    while True:
        query = input('Enter query: ')

        matchedDocuments = handle_query(query)

        if len(matchedDocuments) > 0:
            print(f'Matched documents for query {query}: {matchedDocuments}')
        else:
            print(f'No matches found for query {query}')
