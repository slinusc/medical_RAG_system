import json
import os
from pathlib import Path
from tqdm import tqdm
from elasticsearch import Elasticsearch, helpers

password = os.getenv("ELASTIC_PASSWORD")
password = "btA+=QjPyyUUx0Tq*T9f"

es = Elasticsearch(
    hosts=[{"host": "localhost", "port": 9200, "scheme": "https"}],
    ca_certs="/home/ubuntu/.crts/http_ca.crt",
    basic_auth=("elastic", password),
)

# Define the index name
index_name = "pubmed_index"

# Delete the index if it exists
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Check again if the index exists, and if not, create it
if not es.indices.exists(index=index_name):
    # Define the mapping
    mapping = {
    "mappings": {
        "properties": {
            "content": {
                "type": "text"
            }
        }
    }
}

# Create the index with the defined mapping
es.indices.create(index=index_name, body=mapping)

source_directory = Path('./pubmed/')
error_log_path = Path('./errors.jsonl')  # Pfad zur Fehlerprotokolldatei

def bulk_index_documents(source_directory, index_name, error_log_path):
    if not source_directory.exists():
        print("The source directory does not exist.")
        return

    actions = []  # List to store the documents to be indexed

    # Open the error log file for writing
    with error_log_path.open('w') as error_log:
        # Iterate through each file in the source directory
        for file_name in tqdm(list(os.listdir(source_directory))):
            if file_name.endswith('.jsonl'):
                source_file = source_directory / file_name
                
                # Open and read the JSONL file
                with open(source_file, 'r') as json_file:
                    for line in json_file:
                        try:
                            doc = json.loads(line)
                            
                            # Remove the "embeddings" field from the document
                            if "embeddings" in doc:
                                del doc["embeddings"]
                            
                            action = {
                                "_index": index_name,
                                "_source": doc
                            }
                            actions.append(action)

                            if len(actions) == 200:  # Bulk indexing threshold
                                helpers.bulk(es, actions)
                                actions = []
                        except json.JSONDecodeError as e:
                            # Log the error
                            error_log.write(f"Error in file {file_name}: {e}\n")
                            error_log.write(f"{line}\n")
                        except Exception as e:
                            error_log.write(f"Unexpected error in file {file_name}: {e}\n")
                            error_log.write(f"{line}\n")

        # Index any remaining documents
        if actions:
            helpers.bulk(es, actions)

    print('Indexing complete')

# Call the function to index the documents
bulk_index_documents(source_directory, index_name, error_log_path)

# Count and print the number of documents in the index
count_result = es.count(index=index_name)
print(f"Index contains {count_result['count']} documents.")