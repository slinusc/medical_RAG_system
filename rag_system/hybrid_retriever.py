from elasticsearch import Elasticsearch
import os
import json
from medCPT_encoder import MedCPTCrossEncoder

class HybridRetriever:
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
        self.reranker = MedCPTCrossEncoder()

    def rerank_docs(self, query: str, docs: list):
        """Reranks the documents based on their relevance to the query."""
        scores = self.reranker.score([doc['content'] for doc in docs], query)
        reranked_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return reranked_docs

    def retrieve_docs(self, query: str, top_n: int = 10, k: int = 100):
        """Retrieves documents from Elasticsearch and reranks them, returning only the top N results."""
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

        # Extract documents with full metadata
        docs = [{
            'PMID': hit['_source']['PMID'],
            'title': hit['_source']['title'],
            'content': hit['_source']['content']
        } for hit in response['hits']['hits']]

        # Rerank the documents
        reranked_docs = self.rerank_docs(query, docs)

        # Take only the top N reranked documents
        top_reranked_docs = reranked_docs[:top_n]

        # Construct the final results with reranked scores
        results = {
            f"doc{idx + 1}": {
                'PMID': doc['PMID'],
                'title': doc['title'],
                'content': doc['content'],
                'score': score.item()
            }
            for idx, (doc, score) in enumerate(top_reranked_docs)
        }

        return json.dumps(results, indent=4)

if __name__ == "__main__":
    retriever = HybridRetriever()
    query = "Is Alzheimer's disease hereditary?"
    results = retriever.retrieve_docs(query, k=100, top_n=10)
    print(results)
