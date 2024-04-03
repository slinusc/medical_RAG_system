from sentence_transformers import SentenceTransformer, models
import torch
import time


class TextEmbedder:
    def __init__(self, model_name='dmis-lab/biobert-v1.1', max_length=512):
        if torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"

        self.max_length = max_length

        # Laden des vortrainierten BioBERT-Modells und Hinzufügen eines MEAN-Pooling-Layers
        word_embedding_model = models.Transformer(model_name, max_seq_length=self.max_length)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                                       pooling_mode_mean_tokens=True,
                                       pooling_mode_cls_token=False,
                                       pooling_mode_max_tokens=False)

        self.model = SentenceTransformer(modules=[word_embedding_model, pooling_model], device=self.device)

    def embed(self, text):
        # Text in Embedding umwandeln
        embedding = self.model.encode([text], batch_size=1, show_progress_bar=False)
        return embedding[0]

if __name__ == "__main__":

    embedder = TextEmbedder()
    text = "This is a test sentence."

    start = time.time()
    embedding = embedder.embed(text)
    print(embedding)
    print(time.time() - start)