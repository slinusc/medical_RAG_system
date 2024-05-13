import os
import openai


class evaluateResponseGPT:
    def __init__(self, response, answer):
        self.response = response
        self.correct_answer = answer
        self.model = "gpt-3.5-turbo"
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI(api_key=api_key)
        self.context = self.set_context()

    def set_context(self) -> str:
        return (
            "You will evaluate a response by comparing it to an expert's optimal answer in the biomedical domain. "
            "The evaluation process should include the following steps:"
            "1. Identification of key terms and concepts in both the provided response and the expert's optimal answer. "
            "2. Assessment of the context of the used terms and concepts in the response and the expert's answer. "
            "3. Determination of the accuracy and completeness of the provided response. "
            "Score the response on a scale from 0 to 10, where 0 means completely no overlap with the expert's answer and 10 means a perfect match."
            "Provide the discrete numerical score as your response."
        )
    
    def set_initial_message(self):
        return [{"role": "system", "content": self.context}]
    
    def get_evaluation(self) -> float:
        messages = self.set_initial_message()
        messages.append({"role": "user", "content": f"Response: {self.response}"})
        print(f"Correct answer: {self.response}")
        messages.append({"role": "user", "content": f"Correct answer: {self.correct_answer}. Please score the response above from 0 to 1 based on its accuracy and completeness."})
        print(f"Correct answer: {self.correct_answer}")
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.0
            )
            
            # Correct way to access the message content
            response_content = completion.choices[0].message.content  # Removed incorrect dictionary access
            try:
                score = float(response_content.strip())
            except ValueError:
                score = 0  # Handle the case where the response cannot be converted to float
        except Exception as e:
            print(f"An error occurred during response evaluation: {e}")
            score = 0

        return score/10 # Normalize the score to be between 0 and 1


if __name__ == "__main__":
    response = "Standard treatment for type 2 diabetes is insulin injections and does emphasize lifestyle changes or oral medications like metformin."
    correct_answer = "The standard treatment for type 2 diabetes involves lifestyle modifications such as diet and exercise, complemented by medications like metformin to regulate blood sugar levels."
    evaluator = evaluateResponseGPT(response, correct_answer)
    score = evaluator.get_evaluation()
    print(f"Response score: {score}")