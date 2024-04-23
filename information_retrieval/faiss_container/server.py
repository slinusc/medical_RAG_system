from flask import Flask, request, jsonify
import faiss
import numpy as np

app = Flask(__name__)

# Load the Faiss index (assuming the index has already been created and saved)
index = faiss.read_index("/app/faiss_indices/PM_index.index")

@app.route('/search', methods=['POST'])
def search():
    # Extract the query vectors and the value of k from the POST request
    data = request.get_json()
    queries = np.array(data['queries'], dtype='float32')
    
    # Get the number of nearest neighbors to search for
    k = int(data['k'])
    
    # Perform the search in the Faiss index
    distances, indices = index.search(queries, k)
    
    # Return the response as JSON
    return jsonify(indices=indices.tolist(), distances=distances.tolist())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Accessible over port 5000 on all network interfaces