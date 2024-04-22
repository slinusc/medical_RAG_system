import numpy as np
from pathlib import Path
from tqdm import tqdm  # Importiere tqdm für den Fortschrittsbalken

# Speicherpfad für Zwischendateien festlegen
temp_dir = Path('/home/ubuntu/numpy_arrays/temp_pubmed')
temp_dir.mkdir(exist_ok=True)  # Erstelle den Ordner falls nötig

# Dateien laden und Arrays erstellen
# Um sicherzustellen, dass die Reihenfolge der Dateien übereinstimmt, sortieren wir die Dateinamen
embedding_files = sorted(temp_dir.glob('embeddings_*.npy'))
pubmed_id_files = sorted(temp_dir.glob('pubmed_ids_*.npy'))

# Um die Dimensionen des Embedding Arrays zu bestimmen, laden wir vorab ein Array zur Ermittlung der Dimensionen
if embedding_files:  # Stelle sicher, dass die Liste nicht leer ist
    sample_embedding = np.load(embedding_files[0])
    final_embeddings = np.empty((0, sample_embedding.shape[1]))  # Starte mit einem leeren Array der richtigen Dimension

    # Lade und füge die Embedding Arrays schrittweise zusammen
    for file in tqdm(embedding_files, desc="Lade und konkatiniere Embeddings"):
        embeddings = np.load(file)
        final_embeddings = np.concatenate((final_embeddings, embeddings))
    
    # Speichere die finalen Embeddings sofort nach dem Concatenieren
    output_dir = Path('/home/ubuntu/numpy_arrays')
    output_dir.mkdir(exist_ok=True)  # Erstelle den Zielordner falls nötig
    np.save(output_dir / 'embeddings.npy', final_embeddings)
    
    # Lösche die Embedding-Variablen, um Speicher freizugeben
    del final_embeddings, embeddings

    # Lade und füge die PubMed ID Arrays schrittweise zusammen
    final_pubmed_ids = np.array([], dtype=int)  # Starte mit einem leeren Array
    for file in tqdm(pubmed_id_files, desc="Lade und konkatiniere PubMed IDs"):
        ids = np.load(file)
        final_pubmed_ids = np.concatenate((final_pubmed_ids, ids))

    # Sicherstellen, dass die Länge der beiden Arrays gleich ist
    assert len(final_pubmed_ids) == np.load(output_dir / 'embeddings.npy').shape[0], "Die Länge der Arrays stimmt nicht überein."

    # Speichere die finalen PubMed IDs
    np.save(output_dir / 'pubmed_ids.npy', final_pubmed_ids)

    print("Vorgang abgeschlossen")
else:
    print("Keine Embedding-Dateien gefunden.")
