from flask import Flask, request, jsonify
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from flask_caching import Cache
from model.rag import Rag

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'  # You can choose different types of cache (e.g., 'redis', 'memcached', etc.)
cache = Cache(app)

rag = Rag()

# Initialize your LangChain components here
#qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=None)
qa = rag.make_rag_chain()

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    print(data)
    query_text = data['query']

    response = qa.invoke({"input": query_text})
    return jsonify({'message': response['answer']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)