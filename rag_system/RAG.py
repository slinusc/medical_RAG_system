from bioBERTencoder import TextEncooderBioBERT
from linkBioBERTencoder import TextEncooderLinkBioBERT
from semantic_search_bioBERT import bioBERTretriever
from BM25_search import BM25retriever
from hybrid_search import hybridRertiever # not finished yet
from openAI_chat import Chat


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

    def get_answer(self, question: str)->str:
        retrieved_docs = self.retriever.retrieve_docs(question, self.n_docs)
        
        #TODO: add the retrieved PMID's to the chat

        return self.chat.create_chat(question, retrieved_docs)