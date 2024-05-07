import openai
import os
import json
from typing import List, Dict

class Chat:
    def __init__(self, question_type: int = 1, api_key: str = os.getenv('OPENAI_API_KEY'), model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
        self.context = self.set_context(question_type)

    def set_context(self, question_type: int) -> str:
        base_context = (
            "You are a sophisticated medical assistant designed to synthesize responses "
            "from specific medical documents. Only use the information provided in the "
            "documents to answer questions. The first documents should be the most relevant."
            "Do not use any other information except for the documents provided."
            "When answering questions, always format your response "
            "as a JSON object with fields for 'response', 'used_PMIDs'. "
            "Cite all PMIDs your response is based on in the 'used_PMIDs' field."
            "Please think step-by-step before answering questions and provide the most accurate response possible."
        )

        question_specific_context = {
            1: " Provide a detailed or binary response according to the question's requirement.",
            2: " Your response should only be 'yes', 'no'. If if no relevant documents are found, return 'no_docs_found'.",
            3: " Choose between the given options 1 to 4 and return as 'response' the chosen number. If no relevant documents are found, return the number 5.",
        }

        return base_context + question_specific_context.get(question_type, "")

    def set_initial_message(self) -> List[dict]:
        return [{"role": "system", "content": self.context}]

    def create_chat(self, user_message: str, retrieved_documents: Dict) -> str:
        messages = self.set_initial_message()
        messages.append({"role": "user", "content": f"Answer the following question: {user_message}"})
        
        # Improved readability in document separation
        document_texts = ["PMID {}: {} {}".format(doc['PMID'], doc['title'], doc['content']) for doc in retrieved_documents.values()]
        documents_message = "\n\n".join(document_texts)  # Separating documents with two newlines
        messages.append({"role": "system", "content": documents_message})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.0
            )
            
            response_content = completion.choices[0].message.content
            try:
                response_data = json.loads(response_content)
                formatted_response = {
                    "response": response_data.get("response"),
                    "used_PMIDs": response_data.get("used_PMIDs", []),
                    "retrieved_PMIDs": [doc['PMID'] for doc in retrieved_documents.values()]
                }
                return json.dumps(formatted_response)
            except json.JSONDecodeError:
                return json.dumps({"error": "Invalid JSON format in response.", "response": response_content})
        
        except Exception as e:
            return json.dumps({"error": str(e)})