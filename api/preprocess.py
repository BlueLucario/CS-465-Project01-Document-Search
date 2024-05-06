 # preprocess.py (python)
 # Will Moss with some help from Benjamin Weeg
 # Started 
 # Last edited 2024-05-05 (yyyy mm dd)

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
        return [token.toLowerCase() for token in tokens]

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

    @classmethod
    def stringToSoundex(cls, tokens: List[str]):
        dropCharList = str.maketrans("", "", "aehiouwy")
        for token in tokens:
            #Pop first letter for later
            soundexCode = token[0].toUpperCase()
            token = token[1:].toLowerCase().translate(dropCharList)
            #Get number values
            numToken = ""
            i = 0
            while i < len(token): #for loop
                c = token[i]
                if c in 'BFPV':
                    numToken = numToken+'1'
                elif c in 'CGJKQSXZ':
                    numToken = numToken+'2'
                elif c in 'DT':
                    numToken = numToken+'3'
                elif c=='L':
                    numToken = numToken+'4'
                elif c in 'MN':
                    numToken = numToken+'5'
                elif c=='R':
                    numToken = numToken+'6'
                i += 1
            # Remove adjacent duplicates
            token = numToken[-1]
            if len(numToken) > 1:
                c = numToken[-2]
                i = len(numToken) - 2
                while i >= 0:
                    i = i-1
                    if i >= 0:
                        if c != numToken[i]:
                            c = numToken[i]
                            token = c+token
            length = len(token)
            if length < 3:
                soundexCode = soundexCode + token
                soundexCode.ljust(4, '0')
            elif length > 3:
                soundexCode = soundexCode + token[2]
            elif length == 3:
                soundexCode = soundexCode + token
            token = soundexCode



