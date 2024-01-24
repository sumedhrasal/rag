# from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
# from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from rag import llm_config, data, prompt, rag_objects, logger
from urllib.parse import urlencode, quote_plus
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
import json
import logging
import requests


logger.setup_logger()
log = logging.getLogger(__name__)


def conflate(company_name, structured_data: rag_objects.StructuredResponse, unstructured_data):
    response = {}
    if not structured_data:
        response = get_response_from_unstructured_data(company_name, unstructured_data)
    return response


def get_response_from_unstructured_data(company_name, unstructured_data):
    if data.does_company_data_exists(company_name):
        # Load the document, split it into chunks, embed each chunk and load it into the vector store.
        all_docs = data.load_documents_by_name(company_name)
    else:
        all_docs = []
        for source, text in unstructured_data:
            all_docs.extend([Document(page_content=text, metadata={"source": source})])
    text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    documents = text_splitter.split_documents(all_docs)
    embeddings = OpenAIEmbeddings()
    store = Chroma.from_documents(
        documents, embeddings#, collection_name=company_name
    )
    company_json = get_result_by_prompt(store, prompt.get_company_prompt(company_name), 5)
    financial_json = get_result_by_prompt(store, prompt.get_company_financial_prompt(company_name), 3)
    pest_json = get_result_by_prompt(store, prompt.get_industry_pest_prompt(company_json.get('Industry','')), 3)
    # print(financial_json)
    # print(pest_json)

    response = {
        "Company": {
            "Name": company_json.get('Name',''), 
            "Address": company_json.get('Address','')
        },
        "Industry": company_json.get('Industry',''),
        "Description": company_json.get('Description',''),
        "Leadership": {
            "CEO": company_json.get('CEO',''),
            "CTO": company_json.get('CTO',''),
            "CFO": company_json.get('CFO',''),
            "COO": company_json.get('COO',''),
        },
        "Competitors": company_json.get('Competitors',[]),
        "Financials": financial_json.get('Financials',''),
        "Value Proposition": financial_json.get('Value Proposition',''),
        "PEST": {
            "Political": pest_json.get('Political',''),
            "Economical": pest_json.get('Economical',''),
            "Social": pest_json.get('Social',''),
            "Technological": pest_json.get('Technological','')
        },
    }
    return response


def get_result_by_prompt(store, prompt, k):
    relevant_docs = store.similarity_search(prompt, k)
    chain = load_qa_chain(
        # llm=llm_config.get_model(model_name="text-davinci-002"), 
        llm=llm_config.get_chat_model(),
    )
    result = chain(
        {"input_documents": relevant_docs, "question": prompt}, return_only_outputs=True
    )
    response = result['output_text'].replace("\n","").replace("  ", "")
    try:
        return json.loads(response)
    except json.decoder.JSONDecodeError as e:
        return {}


def fetch_vc_information(company_name, company_url, id):
    _company_url = company_url[company_url.index('//')+2:]
    vc_url = f'https://parsers.vc/startup/{_company_url}'
    print(vc_url)
    params = {'url': vc_url, 'noinlinerefs': 'on', 'nonums': 'on'}
    encoded_data = urlencode(params, quote_via=quote_plus)
    final_url = f'https://www.w3.org/services/html2txt?{encoded_data}'
    response = requests.get(final_url)
    company_context = response.text
    print(len(company_context))

    template = """Context:
    ```
    {context}
    ```
    Using the above context answer the following points.
    - Company Address
    - Year Founded
    - Category/Industry
    - Tags
    - Short Description
    - Full Description
    - Latest Round Data
    - Total Funding
    - Competitors
    and respond back as a JSON object. If you don't have an answer in the provided context leave that field empty.
    """
    vc_prompt = SystemMessagePromptTemplate.from_template(
        template, input_variables = ["context"])

    chat_prompt = ChatPromptTemplate.from_messages(
        [vc_prompt]
    )
    chain = LLMChain(llm=llm_config.get_chat_model(), prompt=chat_prompt)

    result = chain.run(context=company_context if len(company_context) < 10000 else company_context[:10000])
    try:
        result_json = json.loads(result)
        result_json['name'] = company_name
        result_json['url'] = company_url
        result_json['request_id'] = id
        return result_json
    except json.decoder.JSONDecodeError as e:
        return {'name': company_name, 'url': company_url, 'year': '', "industry": "", 
            "tags": "", "short description": "", "long description": "", "latest round": "", 
            "total funding": "", "competitors": [],
            "request_id": id}


# def test(company_name):
#     # question = f" What are the products of {company_name}? and who are {company_name}'s competitors?."
#     prompt_1 = f"""
#     You have access to local data sources containing information about a company. 
#     Given the questions it is your responsibility to retrieve data from the local store 
#     and provide the best possible answers. Your objective is to assist the user in making informed decisions 
#     about the company they are inquiring about. 
#     Please furnish comprehensive responses to each question.
#     1. Provide a concise overview of {company_name}'s products, and the technology they employs for building their products.
#     2. Offer insights into the current state of {company_name}'s products.
#     3. Investigate if {company_name} is generating any revenue and determine the total funding raised by them.
#     4. Define {company_name}'s value proposition.
#     """

#     prompt_2 = f"""
#     You have access to local data sources containing information about a company. 
#     Given the question, it is your responsibility to retrieve data from the local store and provide the best possible answer. 
#     Please furnish comprehensive response to the question. Be thorough in your answer:
#     Question: Do a Political analysis on the transportation and Robo-Taxis industry.
#     """

#     prompt_3 = f"""
#     You have access to local data sources containing information about a company. 
#     Given the question, it is your responsibility to retrieve data from the local store and provide the best possible answer. 
#     Please furnish comprehensive response to the question. Be thorough in your answer:
#     Question: Do an Economic analysis on the transportation and Robo-Taxis industry. 
#     """

#     prompt_4 = f"""
#     You have access to local data sources containing information about a company. 
#     Given the question, it is your responsibility to retrieve data from the local store and provide the best possible answer. 
#     Please furnish comprehensive response to the question. Be thorough in your answer:
#     Question: Do a Social analysis on the transportation and Robo-Taxis industry. 
#     """

#     prompt_5 = f"""
#     You have access to local data sources containing information about a company. 
#     Given the question, it is your responsibility to retrieve data from the local store and provide the best possible answer. 
#     Please furnish comprehensive response to the question. Be thorough in your answer:
#     Question: Do a Technological analysis on the transportation and Robo-Taxis industry. 
#     """

#     response = {'PEST Analysis': {}}
#     for i, prompt in enumerate([prompt_1, prompt_2, prompt_3, prompt_4, prompt_5]):
#         relevant_docs = store.similarity_search(prompt, k=5 if i == 0 else 5)
#         result = chain(
#             {"input_documents": relevant_docs, "question": prompt}, return_only_outputs=True
#         )
#         if i == 1:
#             response['PEST Analysis']['Political'] = result['output_text']
#             sleep(30)
#         elif i == 2:
#             response['PEST Analysis']['Economic'] = result['output_text']
#             sleep(30)
#         elif i == 3:
#             response['PEST Analysis']['Social'] = result['output_text']
#             sleep(30)
#         elif i == 4:
#             response['PEST Analysis']['Technological'] = result['output_text']
#             sleep(30)
#         elif i == 0:
#             answers = result['output_text'].split("\n\n")
#             print(len(answers))
#             if len(answers) > 7:
#                 response['Company'] = answers[1] + answers[2]
#                 response['Competitors'] = answers[3]
#                 response['Industry'] = answers[4]
#                 response['Financials'] = answers[5]
#                 response['Leadership'] = answers[6]
#                 response['Value Proposition'] = answers[7]
#             else:
#                 response['Company'] = result['output_text']
#             sleep(30)
#     store.delete_collection()
