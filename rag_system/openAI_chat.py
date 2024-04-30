import openai
import os
from typing import List, Dict
import json

class Chat:
    def __init__(self, question_type: int = 1, api_key: str = os.getenv('OPENAI_API_KEY'), model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
        self.context = self.set_context(question_type)

    def set_context(self, question_type: int) -> str:
        
        basic_context = (
            "You are a medical assistant. Your task is to provide information "
            "based on specific documents provided to you. Answer the questions "
            "by referring directly to the documents and cite the PMIDs of the documents you used. "
            "1. Go through every dokument and evaluate if one ore more are relevant to answer the question. "
            "2. Answer the question based on the relevant documents."
            "3. If you cannot answer using the documents, state that you cannot answer the question."
            "Your answer should be structured as a JSON object with the answer as 'response' and the PMIDs used as 'used_PMIDs.'"
        )

        if question_type == 1:
            return basic_context + "The 'response' should always be fulltext with referenced PMIDs in brackets. The 'used_PMIDs' should be a list of PMIDs. "
        elif question_type == 2:
            return basic_context + "The 'response' should only be 'yes' or 'no' or 'no_docs_found'. The 'used_PMIDs' should be a list of PMIDs. "

    def set_initial_message(self) -> List[dict]:
        return [{"role": "system", "content": self.context}]

    def create_chat(self, user_message: str, retrieved_documents: Dict) -> str:
        messages = self.set_initial_message()
        messages.append({"role": "user", "content": f"Answer the following question: {user_message}"})

        document_texts = [f"PMID {doc['PMID']}: {doc['title']} {doc['content']}" for doc in retrieved_documents.values()]
        documents_message = " ".join(document_texts)
        messages.append({"role": "system", "content": documents_message})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=300,
                temperature=0.1 # Low temperature to reduce randomness
            )

            response_content = completion.choices[0].message.content
            try:
                # Attempt to parse the response as JSON
                response_data = json.loads(response_content)
                return json.dumps(response_data)  # Directly return the JSON if parsing is successful
            except json.JSONDecodeError:
                # If parsing fails, return a custom error message
                return json.dumps({"error": "Response format is incorrect, expected JSON.", "response": response_content})
        
        except Exception as e:
            return json.dumps({"error": str(e)})
