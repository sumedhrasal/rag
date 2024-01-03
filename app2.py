from time import sleep
from flask import Flask, request, jsonify
from rag import llm_config#, vectorstore
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from rag import data


app = Flask(__name__)


@app.route('/company/batch', methods=['POST'])
def batch_mode():
    # fetch company name
    # check if company exists by searching in the DB 
    #       - if found, load pages
    #       - if not found 
    #       - search on the web 
    #               - if not found, return with no response
    #               - if found, save data into DB and load pages

    # Get the JSON data from the request
    request_data = request.get_json()
    company_name = str(request_data['company']).lower()

    # Load the document, split it into chunks, embed each chunk and load it into the vector store.
    all_docs = data.load_documents_by_name(company_name)
    text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    documents = text_splitter.split_documents(all_docs)
    embeddings = OpenAIEmbeddings()
    store = Chroma.from_documents(
        documents, embeddings#, collection_name=company_name
    )

    # chain = RetrievalQA.from_chain_type(
    chain = load_qa_with_sources_chain(
    # chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm_config.get_model(model_name="text-davinci-002"), 
        # retriever=store.as_retriever()
    )

    # question = f" What are the products of {company_name}? and who are {company_name}'s competitors?."
    prompt_1 = f"""
    You have access to local data sources containing information about a company. 
    Given the questions it is your responsibility to retrieve data from the local store 
    and provide the best possible answers. Your objective is to assist the user in making informed decisions 
    about the company they are inquiring about. 
    Please furnish comprehensive responses to each question.
    1. Provide a concise overview of {company_name}, discussing their products, 
    the year of establishment, their office location, and the technology they employs for building their products.
    2. Offer insights into the current state of {company_name}'s products.
    3. List all competitors or alternatives to {company_name}.
    4. Determine the industry category that best suits {company_name}.
    5. Investigate if {company_name} is generating any revenue and determine the total funding raised by them.
    6. Identify the individuals in {company_name}'s leadership team.
    7. Define {company_name}'s value proposition.
    """

    prompt_2 = f"""
    You have access to local data sources containing information about a company. 
    Given the question, it is your responsibility to retrieve data from the local store and provide the best possible answer. 
    Please furnish comprehensive response to the question. Be thorough in your answer:
    Question: Do a Political analysis on the transportation and Robo-Taxis industry.
    """

    prompt_3 = f"""
    You have access to local data sources containing information about a company. 
    Given the question, it is your responsibility to retrieve data from the local store and provide the best possible answer. 
    Please furnish comprehensive response to the question. Be thorough in your answer:
    Question: Do an Economic analysis on the transportation and Robo-Taxis industry. 
    """

    prompt_4 = f"""
    You have access to local data sources containing information about a company. 
    Given the question, it is your responsibility to retrieve data from the local store and provide the best possible answer. 
    Please furnish comprehensive response to the question. Be thorough in your answer:
    Question: Do a Social analysis on the transportation and Robo-Taxis industry. 
    """

    prompt_5 = f"""
    You have access to local data sources containing information about a company. 
    Given the question, it is your responsibility to retrieve data from the local store and provide the best possible answer. 
    Please furnish comprehensive response to the question. Be thorough in your answer:
    Question: Do a Technological analysis on the transportation and Robo-Taxis industry. 
    """

    response = {'PEST Analysis': {}}
    for i, prompt in enumerate([prompt_1, prompt_2, prompt_3, prompt_4, prompt_5]):
        relevant_docs = store.similarity_search(prompt, k=5 if i == 0 else 5)
        result = chain(
            {"input_documents": relevant_docs, "question": prompt}, return_only_outputs=True
        )
        if i == 1:
            response['PEST Analysis']['Political'] = result['output_text']
            sleep(30)
        elif i == 2:
            response['PEST Analysis']['Economic'] = result['output_text']
            sleep(30)
        elif i == 3:
            response['PEST Analysis']['Social'] = result['output_text']
            sleep(30)
        elif i == 4:
            response['PEST Analysis']['Technological'] = result['output_text']
            sleep(30)
        elif i == 0:
            answers = result['output_text'].split("\n\n")
            print(len(answers))
            if len(answers) > 7:
                response['Company'] = answers[1] + answers[2]
                response['Competitors'] = answers[3]
                response['Industry'] = answers[4]
                response['Finanicals'] = answers[5]
                response['Leadership'] = answers[6]
                response['Value Proposition'] = answers[7]
            else:
                response['Company'] = result['output_text']
            sleep(30)
    store.delete_collection()
    return jsonify({"response":response})


@app.route('/company/live', methods=['POST'])
def live_mode():
    request_data = request.get_json()
    company_name = str(request_data['company']).lower()

    # call crunchbase API here

    return jsonify({"response":"ok"})


if __name__ == '__main__':
    # embeddings = OpenAIEmbeddings()
    # store = Chroma("company", embeddings)
    app.run(host='0.0.0.0', port='8080', debug=True)
