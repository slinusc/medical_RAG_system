import numpy as np
from pathlib import Path
from tqdm import tqdm
import pandas as pd

def concatenate_pubmed_ids(input_dir: Path, output_dir: Path) -> None:
    # Sicherstellen, dass das Ausgabeverzeichnis vorhanden ist
    output_dir.mkdir(exist_ok=True)

    # Laden und Konkatenieren der PubMed ID Arrays
    final_pubmed_ids = np.array([], dtype=int)

    id_files = sorted(input_dir.glob('pubmed_ids_*.npy'))

    if not id_files:
        print("Keine PubMed ID .npy Dateien gefunden.")
        return

    for file in tqdm(id_files, desc="Lade und konkatiniere PubMed IDs"):
        ids = np.load(file)
        final_pubmed_ids = np.concatenate((final_pubmed_ids, ids))

    # Speichern der finalen PubMed IDs
    pd.DataFrame(final_pubmed_ids).to_csv(output_dir / 'concatenated_pubmed_ids.csv', index=False, header=False)
    print("Finale PubMed IDs gespeichert.")

if __name__ == "__main__":
    input_dir = Path('/home/ubuntu/data/numpy_embeddings')
    output_dir = Path('/home/ubuntu/stuhllin/medical_RAG_system/information_retrieval/faiss_container/PMIDs')
    concatenate_pubmed_ids(input_dir, output_dir)
