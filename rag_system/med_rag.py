import json
import time
from openAI_chat import Chat
from bioBERT_retriever import BioBERTRetriever
from bm25_retriever import BM25Retriever
from hybrid_retriever import HybridRetriever
from medCPT_retriever import MedCPTRetriever

class MedRAG:
    def __init__(self, retriever=1, question_type=1, n_docs=10):
        if retriever == 1:
            self.retriever = BioBERTRetriever()
        elif retriever == 2:
            self.retriever = BM25Retriever()
        elif retriever == 3:
            self.retriever = HybridRetriever()
        elif retriever == 4:
            self.retriever = MedCPTRetriever(rerank=True)
        else:
            raise ValueError("Invalid retriever value. Choose 1 for bioBERT, 2 for BM25, or 3 for hybrid.")

        self.chat = Chat(question_type=question_type) # 1 for full text, 2 for yes/no
        self.n_docs = n_docs

    def extract_pmids(self, docs):
        # Extracts PMIDs from the documents and returns them as a list
        return [doc["PMID"] for doc in docs.values()]

    def get_answer(self, question: str) -> str:

        # retrieve the documents timing the retrieval
        start_time_retrieval = time.time()
        retrieved_docs = json.loads(self.retriever.retrieve_docs(question, self.n_docs))
        end_time_retrieval = time.time()

        # extract the PMIDs from the retrieved documents
        pmids = self.extract_pmids(retrieved_docs)

        # the chat response is a json string {'response': '...', 'used_PMIDs': [...]} and timing the generation
        start_time_generation = time.time()
        answer = self.chat.create_chat(question, retrieved_docs)
        end_time_generation = time.time()

        retrieval_time = end_time_retrieval - start_time_retrieval
        generation_time = end_time_generation - start_time_generation

        # now adding the retrieved PMIDs to the response
        try :
            answer = json.loads(answer)
            answer['retrieved_PMIDs'] = pmids
            answer['retrieval_time'] = retrieval_time
            answer['generation_time'] = generation_time
        except:
            return None
        return json.dumps(answer)