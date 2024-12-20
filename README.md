
# Medical RAG System

This repository contains a comprehensive implementation of a Medical Retrieval-Augmented Generation (RAG) system. The system integrates multiple components for document retrieval, question answering, and evaluation, tailored specifically for the medical domain.

## Table of Contents
- [Overview](#overview)
- [File Structure](#file-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Components](#components)
  - [Retrieval System](#retrieval-system)
  - [Question Answering System](#question-answering-system)
  - [Evaluation](#evaluation)
  - [Data Storage](#data-storage)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Medical RAG System is designed to enhance medical information retrieval and provide accurate answers to medical queries. It combines various retrieval methods, including BM25, bioBERT, and hybrid models, with advanced question-answering techniques to ensure precise and relevant results.


## File structure

```plaintext
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
│       │   └── filter_data.ipynb
│       ├── evaluation_pipeline.ipynb
│       ├── explore_questions.ipynb
│       ├── full_text_evaluation.py
│       └── RAG_evaluator.py
├── information_retrieval
│   ├── document_encoding
│   │   ├── bioBERT_encoder.py
│   │   ├── encode_documents.ipynb
│   │   └── medCPT_encoder.py
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
│   ├── bioBERT_encoder.py
│   ├── bioBERT_retriever.py
│   ├── bm25_retriever.py
│   ├── hybrid_retriever.py
│   ├── medCPT_encoder.py
│   ├── medCPT_retriever.py
│   ├── med_rag.py
│   ├── openAI_chat.py
│   └── pipeline.ipynb
├── README.md
├── requirements.txt
└── sys_requirements.txt

```

## Installation

To set up the Medical RAG System, follow these steps:

1. **Clone the Repository**

   ```
   git clone https://github.com/slinusc/medical_RAG_system.git
   cd medical_RAG_system
   ```

2. **Install Dependencies**

   Create a virtual environment and install the required packages:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Download Pre-trained Models**

   Ensure that you download and set up any necessary pre-trained models (e.g., BioBERT, MedCPT).

## Usage

The system can be used for different purposes, including document retrieval, question answering, and evaluation. Each component has its own set of instructions and example notebooks.

### Retrieval System

- **BM25 Retriever**: `rag_system/bm25_retriever.py`
- **BioBERT Retriever**: `rag_system/bioBERT_retriever.py`
- **Hybrid Retriever**: `rag_system/hybrid_retriever.py`

### Question Answering System

- **Medical RAG**: `rag_system/med_rag.py`
- **OpenAI Chat**: `rag_system/openAI_chat.py`

### Evaluation

Evaluation scripts and notebooks are located in the `evaluation/evaluation_QA_system/` directory. Example notebooks are provided to demonstrate the evaluation process.

#### Running an Evaluation

1. **Filter the Data (Optional)**

   If you need to filter your dataset before evaluation, use the provided notebook:

   ```
   evaluation/evaluation_QA_system/dataset_filter/filter_data.ipynb
   ```

2. **Evaluate**
To run the evaluation pipeline, use the evaluation_pipeline.ipynb notebook located in the evaluation/evaluation_QA_system/ directory. This notebook provides a comprehensive guide and setup to evaluate the performance of the RAG system.
## Data Storage



## Contributing

We welcome contributions to enhance the Medical RAG System. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
