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

### BioLinkBERT for Information Retrieval

Die Integration von BioLinkBERT oder ähnlichen Sprachmodellen in ein Information Retrieval (IR) System kann die Genauigkeit und Relevanz der Suchergebnisse erheblich verbessern, insbesondere in spezialisierten Wissensdomänen wie der Biomedizin. Hier sind die grundlegenden Schritte, wie man ein solches Modell in ein IR-System einbinden könnte:

### 1. Auswahl des Information Retrieval Systems
Zuerst muss ein geeignetes IR-System ausgewählt oder entwickelt werden. Dies könnte eine traditionelle Keyword-basierte Suche oder eine fortschrittlichere semantische Suchmaschine sein, die auf Vektorraumsuchen basiert (z.B. Elasticsearch oder Solr mit Vektor-Such-Plugins).

### 2. Vorbereitung des Index
- **Dokumentenvorbereitung**: Alle Dokumente müssen indiziert werden. Dies beinhaltet das Extrahieren von Texten, das Aufbereiten und möglicherweise das Annotieren mit Metadaten.
- **Einbindung von BioLinkBERT**: Verwenden Sie BioLinkBERT, um Texte in hochdimensionale Vektoren zu transformieren, die dann im Suchindex gespeichert werden. Diese Vektoren repräsentieren die semantischen Signaturen der Dokumente.

### 3. Query Processing
- **Abfrage Umwandlung**: Wenn ein Benutzer eine Suchanfrage einreicht, sollte diese Anfrage ebenfalls durch BioLinkBERT verarbeitet werden, um die semantische Repräsentation der Anfrage zu erhalten.
- **Vektorsuche**: Nutzen Sie die generierten Vektoren, um die semantische Nähe zwischen der Suchanfrage und den Dokumenten im Index zu berechnen. Dies kann durch Berechnung von Kosinusähnlichkeiten zwischen den Vektoren erfolgen.

### 4. Ranking und Relevanz-Feedback
- **Relevanz Ranking**: Die Dokumente werden basierend auf ihrer semantischen Nähe zur Anfrage gerankt. Je höher die Ähnlichkeit, desto relevanter das Dokument.
- **Feedback Loop**: Optionales Nutzerfeedback zu den Suchergebnissen kann verwendet werden, um das Modell weiter zu trainieren und die Genauigkeit der Suchergebnisse zu verbessern.

### 5. Einsatz von erweiterten NLP-Techniken
- **Frage-Antwort-Funktionen**: Für spezifische Anfragen, besonders in QA-Systemen, kann BioLinkBERT verwendet werden, um direkt Antworten aus den Texten zu extrahieren, indem es relevante Textpassagen identifiziert und die darin enthaltenen Informationen herausstellt.
- **Zusammenfassungen und Highlighting**: Für längere Dokumente kann BioLinkBERT genutzt werden, um Zusammenfassungen zu erstellen oder Schlüsselinformationen hervorzuheben, die für die Anfrage relevant sind.

### 6. Skalierung und Performance-Optimierung
- **Effizienz**: Beachten Sie, dass die Verarbeitung von Anfragen mit einem vollständigen Sprachmodell rechenintensiv sein kann. Effizienzsteigerungen können durch Techniken wie Quantisierung, Pruning oder den Einsatz spezialisierter Hardware erreicht werden.
- **Parallelisierung**: Um die Geschwindigkeit zu erhöhen, können Anfragen parallelisiert und auf mehreren Servern oder in der Cloud ausgeführt werden.

Die Einbindung von BioLinkBERT in ein IR-System erfordert eine sorgfältige Planung und Optimierung, kann jedoch die Fähigkeit des Systems, thematisch relevante und kontextuell passende Dokumente zu finden, erheblich verbessern.