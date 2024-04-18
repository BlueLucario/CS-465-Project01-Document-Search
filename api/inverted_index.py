import os
from abc import ABC, abstractmethod
from collections import defaultdict
from document import SimpleDocument, AbstractDocument
from typing import List
from nltk.corpus import stopwords

class AbstractInvertedIndex(ABC):
    def __init__(self, documentPath='./documents'):
        self.documentPath = documentPath
        self.indexer = defaultdict(list)
    
    @abstractmethod
    def loadDocuments(self):
        pass

    @abstractmethod
    def loadDocument(self, path):
        pass

    @abstractmethod
    def handleQuery(self, query: str) -> List[AbstractDocument]:
        pass

class SimpleInvertedIndex(AbstractInvertedIndex):
    def __init__(self, documentPath='./documents'):
        super().__init__(documentPath)
        self.stopWords = stopwords.words('english')
        self.loadDocuments() # TODO: Think about loading sequence

    def getTokens(self, data):
        tokens = data.split()

        filteredTokens = []
        for token in tokens:
            token = token.lower()
            if not any(let.isdigit() for let in token) and token not in self.stopWords:
                filteredTokens.append(token)
        
        return filteredTokens

    def _getNextId(self):
        id = 1
        while True:
            yield i
            i += 1
    
    def loadDocuments(self):
        for dirPath, dirNames, files in os.walk(self.documentPath):
            print(f'Found directory: {dirPath}')
            for fileName in files:
                fullPath = os.path.join(dirPath, fileName)
                self.loadDocument(fullPath)                
    
    def loadDocument(self, path):
        document = SimpleDocument(path, id=self._getNextId())
        with open(path, 'r') as file:
            data = file.read()
            tokens = self.getTokens(data)
            
            for token in tokens:
                self.indexer[token].append(document)

    def handleQuery(self, query: str) -> List[AbstractDocument]:
        queryWords = query.split()
        commonDocuments = list(set.intersection(*map(set, [self.indexer[queryWord] for queryWord in queryWords if queryWord not in self.stopWords])))
        return commonDocuments

if __name__ == '__main__':
    invertedIndex = SimpleInvertedIndex()
    query = 'cookie and milk'
    print(f'Results of query {query} = {invertedIndex.handleQuery(query)}')