 # inverted_index.py (python)
 # Will Moss & Benjamin Weeg (Group 1)
 # Started: 
 # Last edited: 2024-05-09 (yyyy mm dd)

import os
from abc import ABC, abstractmethod
from collections import defaultdict
from document import SimpleDocument, AbstractDocument, FlexibleDocument
from typing import List
from nltk.corpus import stopwords
from preprocess import Preprocess

defaultPipeline = [Preprocess.splitByWhitespace, Preprocess.removeEmptyString, Preprocess.toLower]

class AbstractInvertedIndex(ABC):
    _instance = None
    def __init__(self):
        raise RuntimeError('Call getInstance() instead ')

    @classmethod
    def getInstance(cls, **kwargs):
        global defaultPipline
        
        if cls._instance is None:
            print('Creating new inverted index...')
            cls._instance = cls.__new__(cls)
            cls._instance.documentPath = './documents' # Most likely overwritten by child class
            cls._instance.preprocessPipeline = defaultPipeline # Likely overwritten
            cls._instance.indexer = defaultdict(list)
            cls._instance.id = 0

            for property, value in kwargs.items():
                setattr(cls._instance, property, value)

            cls._instance.loadDocuments()
        return cls._instance

    def getTokens(self, data: str):
        assert type(data) is str
        processedTokens = [data]
        for process in self.preprocessPipeline:
            processedTokens = process(processedTokens)
        return processedTokens

    def _getNextId(self):
        id = self.id
        self.id += 1
        return id
        
    def loadDocuments(self):
        for dirPath, dirNames, files in os.walk(self.documentPath):
            print(f'Found directory: {dirPath}')
            for fileName in files:
                fullPath = os.path.join(dirPath, fileName)
                self.loadDocument(fullPath)    

    @abstractmethod
    def loadDocument(self, path):
        pass

    @abstractmethod
    def handleQuery(self, query: str) -> List[AbstractDocument]:
        pass

    @abstractmethod
    def generateStatistics(self) -> dict:
        pass

class SimpleInvertedIndex(AbstractInvertedIndex):
    @classmethod
    def getInstance(cls, documentPath='./documents'):
        return super().getInstance(
            documentPath=documentPath,
            preprocessPipeline=[
                Preprocess.splitByWhitespace,
                Preprocess.removeTokenWithNumber,
                Preprocess.removeEmptyString,
                Preprocess.removeStopwords,
                Preprocess.removeEmptyString,
                Preprocess.stringToSoundex,
            ],
            stopWords=stopwords.words('english')
        )

    def loadDocument(self, path):
        document = SimpleDocument(path, id=self._getNextId())
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
            tokens = self.getTokens(data)
            
            for token in tokens:
                self.indexer[token].append(document)

    def handleQuery(self, query: str) -> List[AbstractDocument]:
        queryWords = query.split()
        postings = [self.indexer[queryWord] for queryWord in queryWords if queryWord not in self.stopWords]
        commonDocuments = list(set.intersection(*map(set,postings))) if len(postings) > 0 else []
        return commonDocuments

    def generateStatistics(self) -> dict:
        return {}

class InvertedIndexWithStats(AbstractInvertedIndex):
    @classmethod
    def getInstance(cls, documentPath='./documents'):
        return super().getInstance(
            documentPath=documentPath, 
            stopWords=stopwords.words('english'),
            documents=[],
            termFrequency={},
            id=1
        )

    def loadDocument(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
            document = FlexibleDocument(path, id=self._getNextId(), 
                                        path=path, data=data)
            self.documents.append(document)
            tokens = self.getTokens(data)
            for token in tokens:
                self.indexer[token].append(document)
                self.termFrequency[token] = self.termFrequency.get(token, 0) + 1

    def handleQuery(self, query: str) -> List[AbstractDocument]:
        queryWords = query.split()
        postings = [self.indexer[queryWord] for queryWord in queryWords if queryWord not in self.stopWords]
        commonDocuments = list(set.intersection(*map(set,postings))) if len(postings) > 0 else []
        return commonDocuments

    def generateStatistics(self) -> dict:
        statistics = {}

        # Report the number of distinct words observed in each document and
        # the total number of words encountered
        statistics['Document stats'] = {}
        for document in self.documents:
            documentStatistics = {}
            documentStatistics['Number of distinct words'] = len(set(document.data.split()))
            documentStatistics['Total number of words'] = len(document.data.split())
            statistics['Document stats'][document.name] = documentStatistics

        # Report the total number of distinct words encountered
        statistics['Total number of distinct words'] = len(self.indexer)

        # Report the total number of words encountered
        statistics['Total number of words encountered'] = sum(self.termFrequency.values())

        # Report the term frequency of each word and the document IDs where 
        # the word occurs (Output the posting list for a term).
        statistics['Term stats'] = {}
        for term, posting in self.indexer.items():
            termStatistics = {}
            termStatistics['Term frequency'] = self.termFrequency[term]
            termStatistics['Document IDs'] = [doc.id for doc in posting]
            statistics['Term stats'][term] = termStatistics

        # Report  the  top  100th,  500th,  and  1000th  most-frequent  
        # word  and  their  frequencies  of occurrence.
        termsSortedByFreq = sorted(self.termFrequency.keys(), key=self.termFrequency.get, reverse=True)
        statistics['Top 100th word'] = termsSortedByFreq[99], self.termFrequency[termsSortedByFreq[99]]
        statistics['Top 500th word'] = termsSortedByFreq[499], self.termFrequency[termsSortedByFreq[499]]
        statistics['Top 1000th word'] = termsSortedByFreq[999], self.termFrequency[termsSortedByFreq[999]]

        # Create postings and assign a term frequency to every document 
        # in the postings list
        # TODO: Figure out what this means
        return statistics

class FlexibleInvertedIndexWithStats(AbstractInvertedIndex):
    @classmethod
    def getInstance(cls, documentPath='./documents', preprocessPipeline=defaultPipeline):
        return super().getInstance(
            documentPath=documentPath, 
            preprocessPipeline=preprocessPipeline,
            stopWords=stopwords.words('english'),
            documents=[],
            termFrequency={},
            id=1
        )

    def loadDocument(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
            document = FlexibleDocument(path, id=self._getNextId(), 
                                        path=path, data=data)
            self.documents.append(document)
            tokens = self.getTokens(data)
            for token in tokens:
                self.indexer[token].append(document)
                self.termFrequency[token] = self.termFrequency.get(token, 0) + 1

    def handleQuery(self, query: str) -> List[AbstractDocument]:
        queryWords = query.split()
        postings = [self.indexer[queryWord] for queryWord in queryWords if queryWord not in self.stopWords]
        commonDocuments = list(set.intersection(*map(set,postings))) if len(postings) > 0 else []
        return commonDocuments

    def generateStatistics(self) -> dict:
        statistics = {}

        # Report the number of distinct words observed in each document and
        # the total number of words encountered
        statistics['Document stats'] = {}
        for document in self.documents:
            documentStatistics = {}
            documentStatistics['Number of distinct words'] = len(set(document.data.split()))
            documentStatistics['Total number of words'] = len(document.data.split())
            statistics['Document stats'][document.name] = documentStatistics

        # Report the total number of distinct words encountered
        statistics['Total number of distinct words'] = len(self.indexer)

        # Report the total number of words encountered
        statistics['Total number of words encountered'] = sum(self.termFrequency.values())

        # Report the term frequency of each word and the document IDs where 
        # the word occurs (Output the posting list for a term).
        statistics['Term stats'] = {}
        for term, posting in self.indexer.items():
            termStatistics = {}
            termStatistics['Term frequency'] = self.termFrequency[term]
            termStatistics['Document IDs'] = [doc.id for doc in posting]
            statistics['Term stats'][term] = termStatistics

        # Report  the  top  100th,  500th,  and  1000th  most-frequent  
        # word  and  their  frequencies  of occurrence.
        termsSortedByFreq = sorted(self.termFrequency.keys(), key=self.termFrequency.get, reverse=True)
        statistics['Top 100th word'] = termsSortedByFreq[99], self.termFrequency[termsSortedByFreq[99]]
        statistics['Top 500th word'] = termsSortedByFreq[499], self.termFrequency[termsSortedByFreq[499]]
        statistics['Top 1000th word'] = termsSortedByFreq[999], self.termFrequency[termsSortedByFreq[999]]

        # Create postings and assign a term frequency to every document 
        # in the postings list
        # TODO: Figure out what this means
        return statistics

class SoundexInvertedIndex(AbstractInvertedIndex):
    @classmethod
    def getInstance(cls, documentPath='./documents'):
        return super().getInstance(
            documentPath=documentPath, 
            preprocessPipeline=[
                Preprocess.splitByWhitespace,
                Preprocess.splitBySpecialCharacter,
                Preprocess.removeTokenWithNumber,
                Preprocess.toLower,
                Preprocess.removeEmptyString,
                Preprocess.stringToSoundex,
            ],
            stopWords=stopwords.words('english'),
            documents=[],
            termFrequency={},
            id=1
        )

    def loadDocument(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
            document = FlexibleDocument(path, id=self._getNextId(), 
                                        path=path, data=data)
            self.documents.append(document)
            tokens = self.getTokens(data)
            for token in tokens:
                self.indexer[token].append(document)
                self.termFrequency[token] = self.termFrequency.get(token, 0) + 1

    def handleQuery(self, query: str) -> List[AbstractDocument]:
        queryWords = query.split()
        postings = [self.indexer[queryWord] for queryWord in queryWords if queryWord not in self.stopWords]
        commonDocuments = list(set.intersection(*map(set,postings))) if len(postings) > 0 else []
        return commonDocuments

    def generateStatistics(self) -> dict:
        statistics = {}

        # Report the number of distinct words observed in each document and
        # the total number of words encountered
        statistics['Document stats'] = {}
        for document in self.documents:
            documentStatistics = {}
            documentStatistics['Number of distinct words'] = len(set(document.data.split()))
            documentStatistics['Total number of words'] = len(document.data.split())
            statistics['Document stats'][document.name] = documentStatistics

        # Report the total number of distinct words encountered
        statistics['Total number of distinct words'] = len(self.indexer)

        # Report the total number of words encountered
        statistics['Total number of words encountered'] = sum(self.termFrequency.values())

        # Report the term frequency of each word and the document IDs where 
        # the word occurs (Output the posting list for a term).
        statistics['Term stats'] = {}
        for term, posting in self.indexer.items():
            termStatistics = {}
            termStatistics['Term frequency'] = self.termFrequency[term]
            termStatistics['Document IDs'] = [doc.id for doc in posting]
            statistics['Term stats'][term] = termStatistics

        # Report  the  top  100th,  500th,  and  1000th  most-frequent  
        # word  and  their  frequencies  of occurrence.
        termsSortedByFreq = sorted(self.termFrequency.keys(), key=self.termFrequency.get, reverse=True)
        statistics['Top 100th word'] = termsSortedByFreq[99], self.termFrequency[termsSortedByFreq[99]]
        statistics['Top 500th word'] = termsSortedByFreq[499], self.termFrequency[termsSortedByFreq[499]]
        statistics['Top 1000th word'] = termsSortedByFreq[999], self.termFrequency[termsSortedByFreq[999]]

        # Create postings and assign a term frequency to every document 
        # in the postings list
        # TODO: Figure out what this means
        return statistics


def getInvertedIndex() -> AbstractInvertedIndex:
    return FlexibleInvertedIndexWithStats.getInstance(preprocessPipeline=[
        Preprocess.splitByWhitespace,
        Preprocess.splitBySpecialCharacter,
        Preprocess.removeTokenWithNumber,
        Preprocess.toLower,
        Preprocess.removeEmptyString,
        Preprocess.removeStopwords,
        #Preprocess.stringToSoundex,
    ])


if __name__ == '__main__':
    invertedIndex = getInvertedIndex()
    import json
    with open('result.json', 'w') as fp:
        json.dump(invertedIndex.generateStatistics(), fp)
    
    # query = 'cookie and milk'
    # print(f'Results of query {query} = {invertedIndex.handleQuery(query)}')
        

