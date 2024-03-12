import json
from langchain.docstore.document import Document
from langchain_community.retrievers import BM25Retriever

class Retriever:
    def __init__(self, json_filepath):
        self.json_filepath = json_filepath
        self.retriever = self.initialize_retriever()

    def initialize_retriever(self):
        with open(self.json_filepath, 'r') as file:
            data = json.load(file)

        texts = [' '.join(item['tokens']) if isinstance(item['tokens'], list) else item['tokens'] for item in data]
        documents = [Document(page_content=text) for text in texts]
        return BM25Retriever.from_documents(documents)

    def retrieve_documents(self, query):
        return self.retriever.get_relevant_documents(query)

# Example usage:
if __name__ == '__main__':
    json_filepath = '../../langchain_notebook/preprocessed_first1000.json'
    query = "what is as a novel candidate for treating COVID-19 via heme oxygenase-1 induction."
    retriever = Retriever(json_filepath)
    result = retriever.retrieve_documents(query)
    print(result)
