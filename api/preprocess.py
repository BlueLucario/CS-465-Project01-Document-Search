 # preprocess.py (python)
 # Will Moss & Benjamin Weeg (Group 1)
 # Started: 
 # Last edited: 2024-05-09 (yyyy mm dd)

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
    
    @classmethod
    def stringToSoundex(cls, tokens: List[str]):
        processedTokens = []
        for token in tokens:
            token = token.upper()
            #Copy first letter for later
            firstLet = token[0]

            #Get number values
            numCode = ""
            for let in token:
                if let in 'AEHIOUWY':
                    numCode += '0'
                elif let in 'BFPV':
                    numCode += '1'
                elif let in 'CGJKQSXZ':
                    numCode += '2'
                elif let in 'DT':
                    numCode += '3'
                elif let in 'L':
                    numCode += '4'
                elif let in 'MN':
                    numCode += '5'
                elif let in 'R':
                    numCode += '6'

            # Remove adjacent duplicates
            i = 0
            while i < len(numCode)-1:
                if numCode[i] == numCode[i+1]:
                    numCode = numCode[:i] + numCode[i+1:]
                else:
                    i += 1
  
            # If first letter's code == leading digit, remove leading digit
            numCode = numCode[1:]

            # Remove all '0's
            numCode = numCode.replace("0", "")

            # Replace first letter and add trailing 0s if necessary
            soundexCode = (firstLet + numCode).ljust(4, '0')
            processedTokens.append(soundexCode[:4])
            
        return processedTokens
