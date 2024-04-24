import openai
import os

class Chat:
    def __init__(self, question=1, api_key=os.getenv('OPENAI_API_KEY'), model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)
        if question == 1:
            self.context = (
                "You are an medical assistant, answering questions and providing information "
                "about the newest developments in the field of medicine by using the provided "
                "content of the retrieved documents. Only answer the questions that are related "
                "to the provided documents. Only use the information from the provided documents. "
                "Do not use any other sources or knowledge. If you aren't able to answer the question with the provided "
                "Dokuments, just say that you cannot answer this question. Your responses will be used for medical purposes, "
                "so please have a definite answer."
            )
        elif question == 2:
            self.context = (
                "You are an medical assistant, answering questions and providing information "
                "about the newest developments in the field of medicine by using the provided "
                "content of the retrieved documents. Only answer the questions that are related "
                "to the provided documents. Only use the information from the provided documents. "
                "Do not use any other sources or knowledge. If you aren't able to answer the question with the provided "
                "Dokuments, just say that you cannot answer this question. Your responses will be used for medical purposes, "
                "so please have a definite answer."
                "- The question should only be answered with yes or no."
            )
        else:
            raise ValueError("Invalid question value. Choose 1 for open answer questions or 2 for yes/no questions.")

    def set_initial_message(self):
        return [
            {"role": "system", "content": self.context}
        ]

    def create_chat(self, user_message, retrieved_documents):
        messages = self.set_initial_message()
        messages.append({"role": "user", "content": f"Answer the following question: {user_message}"})
        messages.append({"role": "assistant", "content": f"Use these documents to answer the question: {str(retrieved_documents)}"})
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"
