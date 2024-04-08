### Investigation of Elasticsearch and MongoDB as Data Storage

#### Elasticsearch 
ElasticSearch is built on Java and utilizes the Lucene search engine. It writes data to inverted indexes using Lucene segments. 
Elasticsearch avoids excessive I/O by creating dedicated transactional index logs, preventing frequent low-level Lucene commits during indexing.

#### MongoDB:
MongoDB, written in C++, uses a memory map file to map on-disk data files to in-memory byte arrays. 
It organizes data using a doubly linked data structure. MongoDB processes shut down in case of low system memory or high resource utilization, ensuring stability

#### Indexes for Full-Text Search in Elasticsearch and MongoDB.

- **Elasticsearch** uses inverted indexes for full-text search. It uses the BM25 algorithm to rank documents based on relevance.
- **MongoDB** uses ...

#### Loading data into Elasticsearch:
1. Created an dense vector index with 768 dimensions for bioBERT embeddings.
2. Indexed the embeddings of the first 50 JSONL files in the dense vector index.
3. Indexing time took: [2:14: 00<00:00, 80.71s/it] for 1'800'000 documents.
4. 
5. Bulk loading (200 docs) turned out to be significantly faster than single document loading.

#### Loading data into MongoDB:
1. Created a collection with bioBERT embeddings.
2. Inserted the embeddings of the first 100 JSONL files into the collection.
3. Inserting time took: [21:06<00:00, 12.66s/it] for 1'795'879 documents.
4. Inserting data (Bulk: 1000 docs) into MongoDB was faster than Elasticsearch.
5. Text indexing for full text search took 14:30 minutes. 

### Retriever Comparison

- **Full text search** using BM25 ranking algorithm.
- **Semantic search** using bioBERT embedding and KNN / Cosine Similarity.
- **Hybrid search** previous ranking using BM25 followed by semantic search and/or DPR.

  (optional)

- **Knowledge Graph** using relations built on citations or other relations. Retrieved by GNN.
