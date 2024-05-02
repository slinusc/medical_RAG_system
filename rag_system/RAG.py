import json
from openAI_chat import Chat
from semantic_search_bioBERT import bioBERTretriever
from BM25_search import BM25retriever
from hybrid_search import hybridRertiever # not finished yet

class RAG:
    def __init__(self, retriever=1, question_type=1, n_docs=10):
        if retriever == 1:
            self.retriever = bioBERTretriever()
        elif retriever == 2:
            self.retriever = BM25retriever()
        elif retriever == 3:
            self.retriever = hybridRertiever()
        else:
            raise ValueError("Invalid retriever value. Choose 1 for bioBERT, 2 for BM25, or 3 for hybrid.")

        self.chat = Chat(question_type=question_type)
        self.n_docs = n_docs

    def extract_pmids(self, docs):
        # Extracts PMIDs from the documents and returns them as a list
        return [doc["PMID"] for doc in docs.values()]

    def get_answer(self, question: str) -> str:
        retrieved_docs = json.loads(self.retriever.retrieve_docs(question, self.n_docs))
        pmids = self.extract_pmids(retrieved_docs)
        # the chat response is a json string {'response': '...', 'used_PMIDs': [...]}
        answer = self.chat.create_chat(question, retrieved_docs)
        # now adding the retrieved PMIDs to the response
        try :
            answer = json.loads(answer)
            answer['retrieved_PMIDs'] = pmids
        except:
            return None
        return json.dumps(answer)