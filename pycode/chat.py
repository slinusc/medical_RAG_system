from openai import OpenAI


class Chat:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-3.5-turbo"
        self.initial_message = []
        self.set_initial_message()

    def set_initial_message(self):
        self.initial_message = [
            {"role": "system",
             "content": f"Answering questions and providing information about the newest developments in the field of "
                        f"medicine."}
        ]

    def create_chat(self, user_message):
        messages = self.initial_message.copy()
        messages.append({"role": "user", "content": user_message})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message


if __name__ == '__main__':
    chat = Chat()
    print(chat.create_chat("Hello there!"))
