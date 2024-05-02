from elasticsearch import Elasticsearch
import os
import json
from bioBERTencoder import TextEncooderBioBERT
from linkBioBERTencoder import TextEncooderLinkBioBERT
import numpy as np

class hybridRertiever:
    def __init__(self, encoder_type: int = 1):
        elastic_password = os.getenv('ELASTIC_PASSWORD')
        self.es = Elasticsearch(
            ['https://localhost:9200'],
            basic_auth=('elastic', elastic_password),
            verify_certs=True,
            ca_certs="/home/ubuntu/.crts/http_ca.crt",
            request_timeout=60
        )
        self.index = "pubmed_index_embedded"
        self.faiss_url = "http://localhost:5000/search"
        if encoder_type == 1:
            self.text_encoder = TextEncooderBioBERT()
        elif encoder_type == 2:
            self.text_encoder = TextEncooderLinkBioBERT()

    def retrieve_vecs(self, query: str, k: int = 1000):
        es_query = {
            "size": k,
            "query": {
                "match": {
                    "content": query 
                }
            },
            "_source": ["PMID", "embeddings"]
        }
        es_response = self.es.search(index=self.index, body=es_query)
        PMIDs = [hit['_source']['PMID'] for hit in es_response['hits']['hits']]
        embeddings = [hit['_source']['embeddings'] for hit in es_response['hits']['hits']]
        return embeddings, PMIDs

    def query_to_vector(self, text: str):
        """Converts text query to a vector using the BioBERT encoder."""
        embedding = self.text_encoder.embed(text)
        return embedding

    @staticmethod
    def rank_vectors_dot_product(query_vector, vector_list, PMIDs, k=10):
        # Compute the dot product of each vector in the list with the query vector
        dot_products = np.dot(vector_list, query_vector)
        # Get the indices that would sort the vectors in descending order of dot products
        sorted_indices = np.argsort(dot_products)[::-1]
        # Return the PMIDs of the top-k vectors, sorted by the computed dot products
        return [PMIDs[i] for i in sorted_indices[:k]]
    
    def get_docs_via_PMIDs(self, PMIDs: list):
        """Retrieves documents from Elasticsearch using a list of PMIDs."""
        query = {
            "size": len(PMIDs),
            "query": {
                "terms": {
                    "PMID": PMIDs
                }
            },
            "_source": ["PMID", "title", "content"]
        }
        return self.es.search(index=self.index, body=query)
    
    def retrieve_docs(self, query: str, return_k: int = 10, search_k: int = 1000):
        embeddings, PMIDS = self.retrieve_vecs(query, search_k)
        query_vector = self.text_encoder.embed(query)
        top_PMIDs = self.rank_vectors_dot_product(query_vector, embeddings, PMIDS, return_k)
        es_response = self.get_docs_via_PMIDs(top_PMIDs)
        results = {}

        for idx, hit in enumerate(es_response['hits']['hits'], 1):
            doc_key = f"doc{idx}"
            results[doc_key] = {
                'PMID': hit['_source']['PMID'],
                'title': hit['_source']['title'],
                'content': hit['_source']['content']
            }

        return json.dumps(results, indent=4)


    

