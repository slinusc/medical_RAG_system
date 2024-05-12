from medCPT_encoder import MedCPTQueryEncoder, MedCPTCrossEncoder
from elasticsearch import Elasticsearch
import os
import requests
import json


class MedCPTRetriever:
    def __init__(self, rerank=True):
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
        self.text_encoder = MedCPTQueryEncoder()
        self.reranker = MedCPTCrossEncoder()
        self.rerank_enabled = rerank

    def query_to_vector(self, text: str):
        """Converts text query to a vector using the medCPT query encoder."""
        embedding = self.text_encoder.encode(text)
        return embedding[0]

    def faiss_request(self, query: str, k: int = 100):
        """Performs a vector search using FAISS with the given query and k."""
        vec = self.query_to_vector(query).tolist()  # Convert numpy array to list
        data = {
            'queries': [vec],  # List of vectors
            'k': k
        }
        response = requests.post(self.faiss_url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        return response.json()

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

    def rerank_docs(self, query: str, docs: list, top_n: int):
        """Reranks the documents based on their relevance to the query and returns the top N."""
        scores = self.reranker.score([doc['content'] for doc in docs], query)
        reranked_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)[:top_n]
        return reranked_docs

    def retrieve_docs(self, query: str, k: int = 20, top_n: int = 10):
        """Retrieves documents relevant to the query using both FAISS and Elasticsearch."""
        response = self.faiss_request(query, k)
        PMIDs = response['PMIDs'][0]
        es_response = self.get_docs_via_PMIDs(PMIDs)

        docs = [{
            'PMID': hit['_source']['PMID'],
            'title': hit['_source']['title'],
            'content': hit['_source']['content']
        } for hit in es_response['hits']['hits']]

        # Apply reranking if enabled
        if self.rerank_enabled:
            reranked_docs = self.rerank_docs(query, docs, top_n)
        
            # only take documents with a score > 0
            reranked_docs = [doc for doc in reranked_docs if doc[1] > 0]

            results = {
                f"doc{idx + 1}": {
                    'PMID': doc['PMID'],
                    'title': doc['title'],
                    'content': doc['content'],
                    'score': score.item()
                }
                for idx, (doc, score) in enumerate(reranked_docs)
            }
        else:
            results = {
                f"doc{idx + 1}": {
                    'PMID': doc['PMID'],
                    'title': doc['title'],
                    'content': doc['content']
                }
                for idx, doc in enumerate(docs[:top_n])
            }

        return json.dumps(results, indent=4)


if __name__ == "__main__":
    retriever = MedCPTRetriever()
    query = "What is the treatment for diabetes?"
    print(retriever.retrieve_docs(query, k=20, top_n=3))
