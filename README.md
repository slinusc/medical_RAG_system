
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
medical_RAG_system/
├── evaluation/
│   ├── evaluation_QA_system/
│   │   ├── RAG_evaluator.py
│   │   ├── evaluation_pipeline.ipynb
│   │   ├── full_text_evaluation.py
│   │   ├── explore_questions.ipynb
│   │   └── dataset_filter/
│   │       └── filter_data.ipynb
│   ├── evaluation_data_storages/
│   │   ├── documentation.md
│   │   ├── elasticsearch/
│   │   │   ├── elastic.ipynb
│   │   │   └── eval_elastic.ipynb
│   │   ├── faiss/
│   │   │   ├── conncatinatior.py
│   │   │   ├── embedding_extractor.py
│   │   │   └── request.ipynb
│   │   └── mongodb/
│   │       ├── eval_mongo.ipynb
│   │       └── mongoDB.ipynb
├── rag_system/
│   ├── bioBERT_retriever.py
│   ├── bm25_retriever.py
│   ├── hybrid_retriever.py
│   ├── medCPT_encoder.py
│   ├── medCPT_retriever.py
│   ├── med_rag.py
│   └── pipeline.ipynb
└── README.md
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

   Ensure that you download and set up any necessary pre-trained models (e.g., bioBERT, CPT).

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

2. **Evaluate with Elasticsearch**

   Use the provided notebooks and scripts to evaluate using Elasticsearch:

   - `evaluation/evaluation_data_storages/elasticsearch/elastic.ipynb`
   - `evaluation/evaluation_data_storages/elasticsearch/eval_elastic.ipynb`

3. **Evaluate with Faiss**

   Use the following notebooks and scripts for evaluation with Faiss:

   - `evaluation/evaluation_data_storages/faiss/request.ipynb`
   - `evaluation/evaluation_data_storages/faiss/conncatinatior.py`
   - `evaluation/evaluation_data_storages/faiss/embedding_extractor.py`

4. **Evaluate with MongoDB**

   Use the MongoDB evaluation notebook:

   - `evaluation/evaluation_data_storages/mongodb/eval_mongo.ipynb`
   - `evaluation/evaluation_data_storages/mongodb/mongoDB.ipynb`

5. **RAG Evaluator Script**

   To run a comprehensive evaluation of the RAG system, use the `RAG_evaluator.py` script:

   ```
   python evaluation/evaluation_QA_system/RAG_evaluator.py
   ```

## Data Storage

- **Elasticsearch**: `evaluation/evaluation_data_storages/elasticsearch/`
- **Faiss**: `evaluation/evaluation_data_storages/faiss/`
- **MongoDB**: `evaluation/evaluation_data_storages/mongodb/`

## Contributing

We welcome contributions to enhance the Medical RAG System. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to reach out if you have any questions or need further assistance!
```
