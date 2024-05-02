from transformers import AutoModel, AutoTokenizer
import torch


class medCPTqueryEncoder:
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
            return outputs.last_hidden_state

if __name__ == "__main__":
    encoder = medCPTqueryEncoder()
    text = "This is a test sentence."
    embedding = encoder.encode(text)
    print(embedding)