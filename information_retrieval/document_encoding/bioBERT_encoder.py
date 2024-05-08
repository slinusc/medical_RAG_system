from sentence_transformers import SentenceTransformer, models
import torch

class bioBERTEncoder:
    def __init__(self, max_length=512):
        if torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"
        
        self.max_length = max_length
        
        word_embedding_model = models.Transformer('dmis-lab/biobert-v1.1', max_seq_length=self.max_length)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                                       pooling_mode_mean_tokens=True,
                                       pooling_mode_cls_token=False,
                                       pooling_mode_max_tokens=False)

        self.model = SentenceTransformer(modules=[word_embedding_model, pooling_model], device=self.device)

    def __call__(self, batch):
        contents = [item["content"] for item in batch]
        embeddings = self.model.encode(contents, batch_size=len(contents), show_progress_bar=False)
        return [{"id": item["id"], "title": item["title"], "content": item["content"], "PMID": item.get("PMID", None), "embeddings": embedding.tolist()} for item, embedding in zip(batch, embeddings)]
