from elasticsearch import Elasticsearch
import os
import requests
import json
from bioBERT_encoder import BioBERTQueryEncooder

class BioBERTRetriever:
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
        self.query_encoder = BioBERTQueryEncooder()

    def query_to_vector(self, text: str):
        """Converts text query to a vector using the BioBERT encoder."""
        embedding = self.query_encoder.encode(text)
        return embedding

    def faiss_query(self, query: str, k: int = 10):
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

    def retrieve_docs(self, query: str, k: int = 10):
        """Retrieves documents relevant to the query using both FAISS and Elasticsearch."""
        response = self.faiss_query(query, k)
        PMIDs = response['PMIDs'][0]  # Assumes PMIDs are returned in a structured list
        es_response = self.get_docs_via_PMIDs(PMIDs)
        results = {}

        # Formatting the response as required
        for idx, hit in enumerate(es_response['hits']['hits'], 1):
            doc_key = f"doc{idx}"
            results[doc_key] = {
                'PMID': hit['_source']['PMID'],
                'title': hit['_source']['title'],
                'content': hit['_source']['content']
            }

        return json.dumps(results, indent=4)