import time
from handle_query import handle_query
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/api/getRelevantDocuments')
def getRelevantDocuments():
    query = request.args.get('query', 'cookie and milk')
    relevantDocs = handle_query(query)
    return json.dumps(relevantDocs, default=lambda x:str(x))

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}