from openai import OpenAI
from .retriever import Retriever

class Chat:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-3.5-turbo"
        self.initial_message = []
        self.set_initial_message()
        # Initialize the retriever with the correct JSON file path
        self.retriever = Retriever("C:/Users/linus/OneDrive/BSc_Data_Science/Semester_4/Big_Data_Project/medical_RAG_system/langchain_notebook/preprocessed_first1000.json")

    def set_initial_message(self):
        self.initial_message = [
            {"role": "system",
             "content": "Answering questions and providing information about the newest developments in the field of "
                        "medicine by using the provided content of the retrieved documents."},
        ]

    def create_chat(self, user_message):
        # Retrieve relevant documents based on the user's message
        retrieved_documents = self.retriever.retrieve_documents(user_message)
        # Combine retrieved documents into a single string to append to the initial message
        # Replace 'content' with the correct attribute name
        retrieved_content = "\n".join([getattr(doc, 'text', 'Document content not available') for doc in retrieved_documents])

        messages = self.initial_message.copy()
        messages.append({"role": "user", "content": user_message})
        # Append the retrieved content as an assistant's message
        messages.append({"role": "assistant", "content": retrieved_content})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content

if __name__ == '__main__':
    chat = Chat()
    user_message = "what is as a novel candidate for treating COVID-19 via heme oxygenase-1 induction."
    response = chat.create_chat(user_message)
    print(response)