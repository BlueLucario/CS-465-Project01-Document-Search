from inverted_index import getInvertedIndex

def generate_statistics() -> dict:
    invertedIndex = getInvertedIndex()
    return invertedIndex.generateStatistics()