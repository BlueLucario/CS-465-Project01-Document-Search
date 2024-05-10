 # generate_statistics.py (python)
 # Will Moss & Benjamin Weeg (Group 1)
 # Started: 
 # Last edited: 2024-05-09 (yyyy mm dd)

from inverted_index import getInvertedIndex

def generate_statistics() -> dict:
    invertedIndex = getInvertedIndex()
    return invertedIndex.generateStatistics()
