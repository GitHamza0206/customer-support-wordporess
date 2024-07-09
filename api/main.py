from flask import Flask, request, jsonify
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from flask_caching import Cache
from flask_cors import CORS
from model.rag import Rag
import os

app = Flask(__name__)
CORS(app)  # This allows all origins
app.config['CACHE_TYPE'] = 'simple'  # You can choose different types of cache (e.g., 'redis', 'memcached', etc.)
cache = Cache(app)

# Create a singleton Rag instance
rag_instance = None

def get_rag_instance():
    global rag_instance
    if rag_instance is None:
        rag_instance = Rag()
    return rag_instance

# Initialize your LangChain components here
qa = None

@app.before_first_request
def initialize_qa():
    global qa
    rag = get_rag_instance()
    qa = rag.make_rag_chain()

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