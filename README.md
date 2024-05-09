# CS 465 Project01 Document Search
**Authors:** William Moss and Benjamin Weeg

## Overview

[Overview]

## Running the project

**Requirements:** Ensure that Docker and npm are installed before running the project. 

This tutorial assumes that you are in the project home directory (i.e the same folder as this README).

To build the project:

1) Build the React frontend server with `npm install`
2) Build the Flask backend server with `cd api && docker build -t searchengine-api-image .`

To run the project:

1) Start the React frontend server with `npm run dev`
2) Open the website at the designited link. It will likely be `localhost:5173`.
3) Run the Flask backend server with `cd api && docker run -dp 5000:5000 --name searchengine-api searchengine-api-image`

To stop the project:

1) Stop the React frontend server with `Ctrl+C`. 

**NOTE:** Do not use `Ctrl+Z` or else the server will continue to run in 
the background and waste resources.

2) Stop the Flask backend server with `cd api && docker stop searchengine-api && docker container prune`. Type Y at the prompt.

**TIP:** Docker Desktop is a useful tool for fixing any bugs with running or 
stopping the Flask backend server.

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
if desired. We recommend reading the JSON on an online viewer like 
[this](https://jsonviewer.stack.hu/).

- All errors and some success responses will be shown in the bottom left 
notification popup.

- The content of the returned documents can be viewed by clicking the document name
(most likely a file path).

The project has the following limitations:

- **All processed documents must be text files.** Invalid file types submitted 
by the frontend will be automatically rejected. However, you can bypass this 
safety feature by uploading invalid documents directly to the folder. This is 
unspecified behavior and will likely lead to poor results.

- **There is no ranked retrieval.** The documents either match the query or don't.

- **Duplicate documents are allowed.** If a document is uploaded twice, the inverted
index will view them as separate documents.

