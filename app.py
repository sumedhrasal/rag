from flask import Flask, request, jsonify
from rag import llm_config, vectorstore
from langchain.chains import LLMChain, RetrievalQA


app = Flask(__name__)


@app.route('/add/context', methods=['POST'])
def add_context():
    # Get the JSON data from the request
    request_data = request.get_json()

    db.add_text(request_data['message'])

    # Process the JSON data (replace with your processing logic)
    response_data = {"message": "Received data"}

    # Return a JSON response
    return jsonify(response_data)


@app.route('/ask', methods=['POST'])
def ask_question():
    # Get the JSON data from the request
    request_data = request.get_json()

    question = request_data['question']
    limit = 5 if request_data.get('limit') is None else int(request_data['limit'])

    llm_flag = True if request_data.get('llm') is None else False

    if llm_flag:
        chain = RetrievalQA.from_chain_type(
            llm=llm_config.get_model(), 
            chain_type="stuff", 
            retriever=db.get_db().as_retriever()
        )
        result = chain.run(question)
        response_data = {"output": "output from DB", "data": result}
    else:
        docs = db.similarity_search(question, limit)
        response_data = {"output": "output from DB", "data": [_.page_content for _ in docs]}

    # Return a JSON response
    return jsonify(response_data)


if __name__ == '__main__':
    class_name = 'Jobs'
    # db = persist.Persist(class_name=class_name)
    db = vectorstore.Store(class_name=class_name)
    app.run(host='0.0.0.0', port='9900', debug=True)
    print('app is now runnning')
