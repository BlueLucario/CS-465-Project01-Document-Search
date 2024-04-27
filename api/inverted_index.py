import os
from abc import ABC, abstractmethod
from collections import defaultdict
from document import SimpleDocument, AbstractDocument
from typing import List
from nltk.corpus import stopwords
from preprocess import Preprocess

class AbstractInvertedIndex(ABC):
	_instance = None
	def __init__(self):
		raise RuntimeError('Call getInstance() instead ')

	@classmethod
	def getInstance(cls, **kwargs):
		if cls._instance is None:
			print('Creating new inverted index...')
			cls._instance = cls.__new__(cls)
			cls._instance.documentPath = './documents' # Most likely overwritten by child class
			cls._instance.indexer = defaultdict(list)
			for property, value in kwargs.items():
				setattr(cls._instance, property, value)
			cls._instance.loadDocuments()
		return cls._instance

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

class SimpleInvertedIndex(AbstractInvertedIndex):
	@classmethod
	def getInstance(cls, documentPath='./documents'):
		return super().getInstance(
			documentPath=documentPath,
			stopWords=stopwords.words('english')
		)

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
			yield id
			id += 1

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

class InvertedIndexWithPreprocessPipeline(AbstractInvertedIndex):
	@classmethod
	def getInstance(cls, documentPath='./documents', preprocessPipeline=[]):
		return super().getInstance(
			documentPath=documentPath,
			preprocessPipeline=preprocessPipeline
		)

	def getTokens(self, data: str):
		assert type(data) is str
		processedTokens = [data]
		for process in self.preprocessPipeline:
			processedTokens = process(processedTokens)
		return processedTokens

	def _getNextId(self):
		id = 1
		while True:
			yield id
			id += 1

	def loadDocument(self, path):
		document = SimpleDocument(path, id=self._getNextId())
		with open(path, 'r') as file:
			data = file.read()
			tokens = self.getTokens(data)	
			for token in tokens:
				self.indexer[token].append(document)

	def handleQuery(self, query: str) -> List[AbstractDocument]:
		queryWords = self.getTokens(queryWords)
		postings = [self.indexer[queryWord] for queryWord in queryWords]
		commonDocuments = list(set.intersection(*map(set,postings))) if len(postings) > 0 else []
		return commonDocuments

def getInvertedIndex() -> AbstractInvertedIndex:
	return InvertedIndexWithPreprocessPipeline.getInstance(preprocessPipeline=[
		Preprocess.splitByWhitespace,
		Preprocess.splitBySpecialCharacter,
		Preprocess.removeTokenWithNumber,
		Preprocess.removeStopwords,
		Preprocess.removeEmptyString, # IMPORTANT: Order matters for this one
		Preprocess.toLower,
	])

if __name__ == '__main__':
	invertedIndex = getInvertedIndex()
	query = 'cookie and milk'
	print(f'Results of query {query} = {invertedIndex.handleQuery(query)}')


