from langchain.document_loaders import TextLoader
from rag import rag_objects
import os


def load_documents_by_name(name):
    directory = os.path.dirname(__file__)
    full_path = os.path.join(directory, 'raw_data', name)
    txt_files = [file for file in os.listdir(full_path) if file.endswith(".txt")]
    all_docs = []
    for file in txt_files:
        docs = TextLoader(os.path.join(full_path, file)).load()
        all_docs.extend(docs)
    return all_docs


def does_company_data_exists(name):
    directory = os.path.dirname(__file__)
    return os.path.exists(os.path.join(directory, 'raw_data', name))


def get_structured_data_by_company(company_name) -> rag_objects.StructuredResponse:
    # data to be filled using CrunchBase
    return None


def get_unstructured_data_by_company(company_name):
    # data to be filled using crawlers
    responses = [{"source_name": ""}] # {"company website": "company description"}
    return responses

