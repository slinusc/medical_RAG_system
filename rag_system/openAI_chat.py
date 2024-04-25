import openai
import os
from typing import List

class Chat:
    def __init__(self, question_type: int = 1, api_key: str = os.getenv('OPENAI_API_KEY'), model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
        self.context = self.set_context(question_type)

    def set_context(self, question_type: int) -> str:
        if question_type == 1:
            return (
                "You are a medical assistant, answering questions and providing information "
                "about the newest developments in the field of medicine by using the provided "
                "content of the retrieved documents. Only answer the questions that are related "
                "to the provided documents. Only use the information from the provided documents. "
                "Do not use any other sources or knowledge. If you aren't able to answer the question with the provided "
                "documents, just say that you cannot answer this question. Your responses will be used for medical purposes, "
                "so please have a definite answer."
            )
        elif question_type == 2:
            return (
                "You are a medical assistant, answering questions and providing information "
                "about the newest developments in the field of medicine by using the provided "
                "content of the retrieved documents. Only answer the questions that are related "
                "to the provided documents. Only use the information from the provided documents. "
                "Do not use any other sources or knowledge. If you aren't able to answer the question with the provided "
                "documents, just say that you cannot answer this question. Your responses will be used for medical purposes, "
                "so please have a definite answer."
                "- The question should only be answered with yes or no."
            )
        else:
            raise ValueError("Invalid question type. Choose 1 for open answer questions or 2 for yes/no questions.")

    def set_initial_message(self) -> List[dict]:
        return [{"role": "system", "content": self.context}]

    def create_chat(self, user_message: str, retrieved_documents: List[str]) -> str:
        messages = self.set_initial_message()
        messages.append({"role": "user", "content": f"Answer the following question: {user_message}"})
        messages.append({"role": "system", "content": f"Use these documents to answer the question: {' '.join(retrieved_documents)}"})
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=200,
                temperature=0.0 # 0.0 for deterministic completions wihout "creativity".
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"