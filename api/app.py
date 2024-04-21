from handle_query import handle_query
from upload_document import upload_document
from flask import Flask, request
from markupsafe import escape
import json
from pathlib import Path
Path('my_file.mp3').suffix == '.mp3'

app = Flask(__name__)

@app.route('/api/relevantDocuments/<query>', methods=['GET'])
def getRelevantDocuments(query):
    relevantDocs = handle_query(escape(query))
    return json.dumps(relevantDocs, default=lambda x:str(x))

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
