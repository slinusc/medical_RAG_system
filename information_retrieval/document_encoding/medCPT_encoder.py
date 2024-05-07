import torch
from transformers import AutoTokenizer, AutoModel
from typing import List, Dict

class medCPTArticleEncoder:
    def __init__(self, max_length=512):
        if torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"
        
        self.max_length = max_length
        self.model = AutoModel.from_pretrained("ncbi/MedCPT-Article-Encoder")
        self.tokenizer = AutoTokenizer.from_pretrained("ncbi/MedCPT-Article-Encoder")

    def __call__(self, batch: List[Dict]) -> List[Dict]:
        encoded_articles = []

        with torch.no_grad():
            # Extract the article content from the batch
            articles = [item["content"] for item in batch]
            
            # Tokenize the articles
            encoded = self.tokenizer(
                articles, 
                truncation=True, 
                padding=True, 
                return_tensors='pt', 
                max_length=self.max_length,
            )
            
            # Encode the articles (use the [CLS] token as the representation)
            outputs = self.model(**encoded)
            embeddings = outputs.last_hidden_state[:, 0, :]

        for i, item in enumerate(batch):
            encoded_articles.append({
                "id": item["id"],
                "title": item["title"],
                "content": item["content"],
                "PMID": item.get("PMID", None),
                "embedding": embeddings[i].tolist()
            })

        return encoded_articles
