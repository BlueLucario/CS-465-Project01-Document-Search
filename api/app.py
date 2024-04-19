import time
from handle_query import handle_query
from flask import Flask, request
from markupsafe import escape
import json

app = Flask(__name__)

@app.route('/api/getRelevantDocuments/<query>')
def getRelevantDocuments(query):
    relevantDocs = handle_query(escape(query))
    return json.dumps(relevantDocs, default=lambda x:str(x))

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}