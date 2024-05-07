from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
import torch


class MedCPTQueryEncoder:
    def __init__(self, model_name='ncbi/MedCPT-Query-Encoder', max_length=512):
        if torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"

        self.max_length = max_length

        # Load pretrained MedCPT-Query-Encoder model and tokenizer
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def encode(self, text):
        with torch.no_grad():
            # Tokenize the text
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=self.max_length).to(self.device)
            # Pass the inputs through the model
            outputs = self.model(**inputs)
            # Return the last hidden states
            return outputs.last_hidden_state[:, 0, :]


class MedCPTCrossEncoder:
    def __init__(self, model_name='ncbi/MedCPT-Cross-Encoder'):
        if torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"

        # Load pretrained Cross-Encoder model and tokenizer
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def score(self, articles, query):
        pairs = [[query, article] for article in articles]

        with torch.no_grad():
            encoded = self.tokenizer(
                pairs,
                truncation=True,
                padding=True,
                return_tensors="pt",
                max_length=512,
            ).to(self.device)

            logits = self.model(**encoded).logits.squeeze(dim=1)
        return logits


if __name__ == "__main__":
    
    cross_encoder = MedCPTCrossEncoder()

    query = "What is the treatment for diabetes?"

    articles = [
        "Diabetes is a chronic disease that occurs when the body is unable to produce enough insulin or use it effectively. Treatment for diabetes includes lifestyle changes, such as diet and exercise, as well as medications like insulin and oral hypoglycemic drugs.",
        "The treatment for diabetes involves managing blood sugar levels through diet, exercise, and medication. Insulin therapy, oral medications, and lifestyle changes are common approaches to managing diabetes.",
        "Diabetes treatment typically involves a combination of diet, exercise, and medication. Insulin therapy, oral medications, and lifestyle changes are key components of managing diabetes.",
    ]

    scores = cross_encoder.score(articles, query)

    for i, (article, score) in enumerate(zip(articles, scores)):
        print(f"Article {i+1}: {article}")
        print(f"Score: {score:.4f}\n")
