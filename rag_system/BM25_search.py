from elasticsearch import Elasticsearch
import os
import json

class BM25retriever:
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

    def retrieve_docs(self, query: str, k: int = 10):
        es_query = {
            "size": k,
            "query": {
                "match": {
                    "content": query 
                }
            },
            "_source": ["PMID", "title", "content"]
        }
        # Execute the search query
        response = self.es.search(index=self.index, body=es_query)
        
        # Format the results into the desired JSON structure
        results = {}
        for idx, doc in enumerate(response['hits']['hits'], 1):
            doc_key = f"doc{idx}"
            results[doc_key] = {
                'PMID': doc['_source']['PMID'],
                'title': doc['_source']['title'],
                'content': doc['_source']['content']
            }

        return json.dumps(results, indent=4)