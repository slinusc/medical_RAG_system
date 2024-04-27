from elasticsearch import Elasticsearch
import os
import requests
import json
from bioBERTencoder import TextEncooderBioBERT
from BM25_search import BM25retriever
import numpy as np

class hybridRertiever:
    def __init__(self):
        elastic_password = os.getenv('ELASTIC_PASSWORD')
        self.es = Elasticsearch(
            ['https://localhost:9200'],
            basic_auth=('elastic', elastic_password),
            verify_certs=True,
            ca_certs="/home/ubuntu/.crts/http_ca.crt",
            request_timeout=60
        )
        self.index = "pubmed_index"
        self.faiss_url = "http://localhost:5000/search"
        self.BM25_retriever = BM25retriever()

    #TODO: create elastic index which contains embeddings of the documents

    def retrieve_docs(self, query, k=10, bm25_docs=1000) -> json:
        BM25_response = self.BM25_retriever.retrieve_docs(query, bm25_docs)
        BM25_PMIDs = [doc['PMID'] for doc in BM25_response.values()]



    

