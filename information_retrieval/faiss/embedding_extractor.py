import numpy as np
import json
import gc  # Garbage Collector importieren
from pathlib import Path
from tqdm import tqdm

def process_files(files):
    pubmed_ids = []
    embeddings = []
    for file_name in tqdm(files, desc="Verarbeite Dateien", leave=False):
        with open(file_name, 'r') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    pubmed_ids.append(int(data.get('PMID', 0)))  # Konvertierung zu Integer mit Standardwert 0
                    embeddings.append(data.get('embeddings', []))  # Standardwert leere Liste
                except json.JSONDecodeError as e:
                    print(f"Fehler beim Decodieren von JSON in Datei {file_name}: {e}")
    return pubmed_ids, embeddings

source_directory = Path('/home/ubuntu/pubmed')
jsonl_files = list(source_directory.glob('*.jsonl'))
batch_size = 15  # Maximale Anzahl an Dateien pro Batch

# Speicherpfade für Zwischendateien
temp_dir = Path('/home/ubuntu/temp_pubmed')
temp_dir.mkdir(exist_ok=True)  # Stelle sicher, dass das Verzeichnis existiert

# Verarbeite Dateien in Batches und speichere Zwischenergebnisse
for i in tqdm(range(0, len(jsonl_files), batch_size), desc="Verarbeite Batches"):
    batch_files = jsonl_files[i:i + batch_size]
    batch_pubmed_ids, batch_embeddings = process_files(batch_files)
    # Speichere die Batch-Daten in temporären Dateien
    np.save(temp_dir / f'embeddings_{i // batch_size}.npy', batch_embeddings)
    np.save(temp_dir / f'pubmed_ids_{i // batch_size}.npy', batch_pubmed_ids)
    # Lösche die Listen, um den Speicher freizugeben
    del batch_pubmed_ids, batch_embeddings
    gc.collect()  # Fordere die Garbage Collection explizit an

# Lade alle Zwischendateien und konkateniere die Arrays
final_embeddings = np.concatenate([np.load(file) for file in temp_dir.glob('embeddings_*.npy')])
final_pubmed_ids = np.concatenate([np.load(file) for file in temp_dir.glob('pubmed_ids_*.npy')])

# Speichere die finalen Arrays
np.save('embeddings.npy', final_embeddings)
np.save('pubmed_ids.npy', final_pubmed_ids)

# Aufräumen: Lösche die temporären Dateien
for file in temp_dir.glob('*.npy'):
    file.unlink()
temp_dir.rmdir()  # Entferne das Verzeichnis, falls es leer ist
