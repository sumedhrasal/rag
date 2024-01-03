from langchain.document_loaders import TextLoader
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

