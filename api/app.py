 # app.py (python)
 # Will Moss & Benjamin Weeg
 # Started 
 # Last edited 2024-05-09 (yyyy mm dd)

from handle_query import handle_query
from upload_document import upload_document
from generate_statistics import generate_statistics
from get_document_content import get_document_content
from flask import Flask, request
from markupsafe import escape
import json
from pathlib import Path

app = Flask(__name__)

handle_query("") # Loads inverted index on startup

@app.route('/api/relevantDocuments/<query>', methods=['GET'])
def getRelevantDocuments(query):
    relevantDocs = handle_query(str(escape(query)))
    return json.dumps(relevantDocs, default=lambda x:vars(x))

@app.route('/api/relevantDocuments', methods=['POST'])
def addRelevantDocument():
    if 'file' not in request.files:
        return "File not submitted", 400

    file = request.files['file']

    if Path(file.filename).suffix != '.txt':
        return "Invalid file type", 400

    try:
        upload_document(file)
    except RuntimeError:
        return "File not uploaded successfully", 500

    return 'File uploaded successfully!', 200

@app.route('/api/statistics', methods=['GET'])
def generateStatistics():
    try:
        return json.dumps(generate_statistics())
    except RuntimeError:
        return "Statistics not generated successfully", 500

@app.route('/api/documentContent/<id>', methods=['GET'])
def getDocumentContent(id):
    try:
        documentContent = get_document_content(str(escape(id)))
        return json.dumps(documentContent)
    except RuntimeError:
        return f"Unable to retrieve the content of document {id}", 500

if __name__ == "__main__":
    app.run(debug=True)
