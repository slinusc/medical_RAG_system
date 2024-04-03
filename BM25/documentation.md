### Investigation of underlying architecture of Elasticsearch and MongoDB.

#### Elasticsearch:
ElasticSearch is built on Java and utilizes the Lucene search engine. It writes data to inverted indexes using Lucene segments. 
Elasticsearch avoids excessive I/O by creating dedicated transactional index logs, preventing frequent low-level Lucene commits during indexing.

#### MongoDB:
MongoDB, written in C++, uses a memory map file to map on-disk data files to in-memory byte arrays. 
It organizes data using a doubly linked data structure. MongoDB processes shut down in case of low system memory or high resource utilization, ensuring stability

#### Conclusion:
Elasticsearch is more efficient in terms of I/O operations and memory management compared to MongoDB.

### Indexes for Full-Text Search in Elasticsearch and MongoDB.

#### Elasticsearch:
Elasticsearch uses inverted indexes for full-text search. It uses the BM25 algorithm to rank documents based on relevance.

#### Loading data into Elasticsearch:
1. Created an dense vector index with 768 dimensions for bioBERT embeddings.
2. Indexed the embeddings of the first 50 JSONL files in the dense vector index.
3. Indexing time took: [31:25<00:00, 37.71s/it] for 709'071 documents.
4. 
3. Bulk loading (400 docs) turned out to be significantly faster than single document loading.


#### Loading data into MongoDB:
1. Created a collection with bioBERT embeddings.
2. Inserted the embeddings of the first 100 JSONL files into the collection.
3. Inserting time took: [21:06<00:00, 12.66s/it] for 1'795'879 documents.
4. Inserting data (Bulk: 1000 docs) into MongoDB was faster than Elasticsearch.
5. Text indexing will be implemented in the next step.