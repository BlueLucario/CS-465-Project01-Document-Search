# CS 465 Project01 Document Search
**Authors:** William Moss and Benjamin Weeg


## Overview
A simple Information Retrieval (IR) system for document collection processing.

Text Processing:
We use a series of tokenization and normalization steps, 
removing digits and special characters to streamline text analysis.

Statistics: 
Generated statistics on word frequency and document occurrence.
The preview shows some key metrics and the full raw data is available for download.


## Running the project

**Requirements:** Ensure that Docker and npm are installed before running the project. 

This tutorial assumes that you are in the project home directory (i.e the same folder as this README).

To build the project:

1) Build the React frontend server with `npm install`
2) Build the Flask backend server with `npm run build-api` or `cd api && docker build -t searchengine-api-image . && cd ..`

To run the project:

1) Run the Flask backend server with `npm run start-api` or `cd api && docker run -dp 5000:5000 --name searchengine-api searchengine-api-image && cd ..`
2) Start the React frontend server with `npm run dev`
3) Open the website at the designated link (likely `localhost:5173`).

To stop the project:

1) Stop the React frontend server with `Ctrl+C`. 

**NOTE:** Do not use `Ctrl+Z` or else the server will continue to run in 
the background and waste resources.

2) Stop the Flask backend server with `npm run stop-api` or `cd api && docker stop searchengine-api && docker container prune && cd ..`. Type Y at the prompt.

**TIP:** Docker Desktop is a useful tool for fixing any bugs with running or stopping the Flask backend server manually.


## Features and Limitations

The project has the following capabilities:

- Query terms are handled via boolean retrieval. For example, the query `X Y Z` 
is handled as `X AND Y AND Z`. 

- Queries and documents are tokenized in the same manner. The current 
inverted index splits terms by any non-alphabetic character (including numbers). 
The inverted index also removes any stopwords and is case-insensitive.

- The inverted index is modular. You can change between inverted indexes in the 
`getInvertedIndex()` function in `api/inverted_index.py`.  

**TIP:** You can add soundex capabilities by using the `SoundexInvertedIndex`.

- The tokenization algorithm is modular. You can modify the algorithm in 
the `getInvertedIndex()` function with the `Preprocess` methods. 

- The inverted index is built once the Flask backend server is loaded. It does 
not wait until the first frontend request. **A frontend request will result in a 500
error if the inverted index is not yet built.**

- The statistics summary can be viewed from the `Show Statistics` button at the 
bottom right of the frontend website. The full statistics JSON can be downloaded 
if desired. We recommend reading the JSON with an online viewer like 
[this](https://jsonviewer.stack.hu/).

- All errors and certain success responses will be shown in the bottom left 
notification popup.

- The content of the returned documents can be viewed by clicking the document name
(i.e the file path).

The project has the following limitations:

- **All processed documents must be text files.** Invalid file types submitted 
by the frontend will be automatically rejected. However, you can bypass this 
safety feature by uploading invalid documents directly to the folder. This is 
unspecified behavior and will likely lead to poor results.

- **There is no ranked retrieval.** The documents either match the query or don't.

- **Duplicate documents are allowed.** If a document is uploaded twice, the inverted
index will view them as separate documents.

- **Documents cannot be deleted once uploaded.** 

- **Server errors (500) are poorly formatted.** There is no logic to prettify server
errors.


## Implementation Details

- All inverted indexes extend the AbstractInvertedIndex for a consistent interface. 

- The dictionary (i.e terms) is implemented with a dictionary (i.e HashMap) 
with the term as its key and the posting as its value. This ensures that lookup 
is O(1) time complexity without the need for sorting. The posting is a list of
Document objects. The Document objects are appended sequentially, so the posting
list is always sorted by id.

- The inverted index follows the singleton pattern. This means that only 1
inverted index is ever built and used.

- The statistics is lazily generated upon request. 

- The algorithms for tokenization is contained in the Preprocess class. All algorithms
take a list of tokens as its input and returns a new list of tokens. For example, 
the `removeTokenWithNumber` function takes a list of tokens and only returns those
without a number. This allows for quick and clear modifications to the tokenization
design. 

- A Dockerfile is made for the Flask backend server ensure a consistent runtime
environment. This decision was made after frequent bugs made collaboration difficult.
A Dockerfile was not made for the React backend server because of the simplicity 
and wide-adoption of npm. 


## Extra Credit

- **Document can be added to the inverted index during runtime.** This is done via the upload button. Remember that the document must be a text file.

- **A soundex inverted index is available for use.** To use the soundex inverted index, go to `getInvertedIndex()` at `api/inverted_index.py` and replace the inverted index with `SoundexInvertedIndex` with the same parameters. Remember to rebuild the project by following the above instructions. 

- **The contents of the retrieved documents can be viewed in the browser.** This is done by clicking the document name (i.e the filepath). A popup will appear with the document's contents. 