import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from flask_caching import Cache
from flask_cors import CORS
from model.rag import Rag
from dotenv import load_dotenv
load_dotenv() 

app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Create a singleton Rag instance
rag_instance = None
qa = None
is_initialized = False

def get_rag_instance():
    global rag_instance
    if rag_instance is None:
        rag_instance = Rag()
    return rag_instance

def initialize_qa():
    global qa, is_initialized
    if not is_initialized:
        rag = get_rag_instance()
        qa = rag.make_rag_chain()
        is_initialized = True

@app.before_request
def before_request():
    initialize_qa()

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    print(data)
    query_text = data['query']

    response = qa.invoke({"input": query_text})
    return jsonify({'message': response['answer']})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)