from typing import List

class Preprocess:
    @classmethod
    def splitByWhitespace(cls, tokens: List[str]):
        processedTokens = []
        for token in tokens:
            processedTokens += token.split()
        
        return processedTokens

    @classmethod
    def removeTokenWithNumber(cls, tokens: List[str]):        
        return [token for token in tokens if not any(char.isdigit() for char in token)]

    @classmethod
    def removeStopwords(cls, tokens: List[str]):
        from nltk.corpus import stopwords
        stopWords = stopwords.words('english')
        
        return [token for token in tokens if token not in stopWords]
    
    @classmethod
    def toLower(cls, tokens: List[str]):
        return [token.lower() for token in tokens]
    
    @classmethod
    def splitBySpecialCharacter(cls, tokens: List[str]):
        import re
        processedTokens = []

        for token in tokens:
            processedTokens += re.split('[^a-zA-Z]', token)
        
        return processedTokens
    
    @classmethod
    def removeEmptyString(cls, tokens: List[str]):
        return [token for token in tokens if token.strip() != '']