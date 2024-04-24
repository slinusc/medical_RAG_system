Here is our current file structure.
```
.
├── information_retrieval
│   ├── elastic_container
│   │   ├── elastic.ipynb
│   │   ├── ingest_data.py
│   │   └── start_elasticsearch.sh
│   ├── evaluation
│   │   ├── data_storage
│   │   │   ├── documentation.md
│   │   │   ├── elasticsearch
│   │   │   │   ├── elastic.ipynb
│   │   │   │   └── eval_elastic.ipynb
│   │   │   ├── faiss
│   │   │   │   ├── conncatinatior.py
│   │   │   │   ├── embedding_extractor.py
│   │   │   │   └── request.ipynb
│   │   │   └── mongodb
│   │   │       ├── eval_mongo.ipynb
│   │   │       └── mongoDB.ipynb
│   │   └── retriever
│   │       └── dataset_filter
│   │           ├── filter_data.ipynb
│   │           └── Q&A.py
│   ├── faiss_container
│   │   ├── docker-compose.yml
│   │   ├── faiss_insert_data.ipynb
│   │   └── server.py
│   └── ray
│       ├── embedd_docs.ipynb
│       └── Embedding.py
├── rag_system
│   ├── chat.py
│   └── llm.py
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


```
