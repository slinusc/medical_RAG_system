import json
from openAI_chat import Chat
from bioBERT_retriever import BioBERTRetriever
from bm25_retriever import BM25Retriever
from hybrid_retriever import HybridRetriever
from medCPT_retriever import SemanticRetrieverMedCPT

class MedRAG:
    def __init__(self, retriever=1, question_type=1, n_docs=10):
        if retriever == 1:
            self.retriever = BioBERTRetriever()
        elif retriever == 2:
            self.retriever = BM25Retriever()
        elif retriever == 3:
            self.retriever = HybridRetriever()
        elif retriever == 4:
            self.retriever = SemanticRetrieverMedCPT(rerank=True)
        else:
            raise ValueError("Invalid retriever value. Choose 1 for bioBERT, 2 for BM25, or 3 for hybrid.")

        self.chat = Chat(question_type=question_type) # 1 for full text, 2 for yes/no
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