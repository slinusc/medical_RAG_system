Here is our current file structure.
```
├── evaluation
│   ├── evaluation_data_storages
│   │   ├── documentation.md
│   │   ├── elasticsearch
│   │   │   ├── elastic.ipynb
│   │   │   └── eval_elastic.ipynb
│   │   ├── faiss
│   │   │   ├── conncatinatior.py
│   │   │   ├── embedding_extractor.py
│   │   │   └── request.ipynb
│   │   └── mongodb
│   │       ├── eval_mongo.ipynb
│   │       └── mongoDB.ipynb
│   └── evaluation_QA_system
│       ├── dataset_filter
│       │   ├── filter_data.ipynb
│       │   └── Q&A.py
│       ├── evaluation_pipeline.ipynb
│       ├── explore_questions.ipynb
│       └── RAG_evaluator.py
├── information_retrieval
│   ├── document_encoding
│   │   ├── embedd_docs.ipynb
│   │   └── Embedding.py
│   ├── elastic_container
│   │   ├── elastic.ipynb
│   │   ├── ingest_data.py
│   │   └── start_elasticsearch.sh
│   └── faiss_container
│       ├── docker-compose.yml
│       ├── Dockerfile
│       ├── faiss_insert_data.ipynb
│       └── server.py
├── rag_system
│   ├── bioBERTencoder.py
│   ├── BM25_search.py
│   ├── hybrid_search.py
│   ├── linkBioBERTencoder.py
│   ├── medCPTEncoder.py
│   ├── medCPTRetriever.py
│   ├── openAI_chat.py
│   ├── pipe.drawio.png
│   ├── pipeline.ipynb
│   ├── RAG.py
│   └── semantic_search_bioBERT.py
├── README.md
└── web_interface
    ├── app.py
    ├── pycode
    │   ├── chat.py
    │   ├── __init__.py
    │   └── retriever.py
    ├── static
    │   ├── css
    │   │   ├── style_chat.css
    │   │   └── styles_login.css
    │   ├── images
    │   │   ├── google.png
    │   │   └── logo4.jpg
    │   └── js
    │       ├── chat.js
    │       └── login.js
    └── templates
        ├── chat.html
        └── login_page.html

19 directories, 46 files


```
