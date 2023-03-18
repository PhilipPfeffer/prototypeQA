import os
from pypdf import PdfReader
import openai
import env  # This is a file that contains the OpenAI API key
from collections import defaultdict

class QuestionProcessor:
    def __init__(self, pdf_directory, questions_path):
        self.pdf_directory = pdf_directory
        self.questions_path = questions_path
        self.questions = []
        self.TEXT_CHUNK_LEN = 1000
        openai.api_key = env.OPENAI_API_KEY
    
    def read_questions(self):
        with open(self.questions_path, "r") as file:
            self.questions = [line.strip() for line in file.readlines()]

    def process_pdf(self, pdf_path):
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            full_text = "".join(page.extract_text() for page in reader.pages)
        return full_text

    def get_answers(self, full_text, question):
        all_answers = defaultdict(list)
        for i in range(0, len(full_text), self.TEXT_CHUNK_LEN):
            chunk = full_text[i:i + self.TEXT_CHUNK_LEN]
            prompt = f"Given the following text, give a direct answer with no explanation:\n\n{chunk}\n\nQuestion: {question}\n\nAnswer (reply 'NONE' if the text does not contain the answer):"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )

            answer = response["choices"][0]["message"]["content"].strip()
            if "none" not in answer.lower():
                all_answers[question].append(answer)
        return all_answers

    def find_most_likely_answer(self, question, all_answers):
        potential_answers = ', '.join(all_answers[question])
        prompt = f"Here are potential answers to the question '{question}', which is most likely to be correct given frequency of appearance? Respond with only the answer and no explanatory text. Potential answers: [{potential_answers}]"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )

        most_likely_answer = response["choices"][0]["message"]["content"].strip()
        return most_likely_answer

    def process_questions(self):
        self.read_questions()
        for pdf_file in os.listdir(self.pdf_directory):
            if pdf_file.endswith(".pdf"):
                pdf_path = os.path.join(self.pdf_directory, pdf_file)
                full_text = self.process_pdf(pdf_path)

                for question in self.questions:
                    all_answers = self.get_answers(full_text, question)
                    most_likely_answer = self.find_most_likely_answer(question, all_answers)
                    print(f"File: {pdf_file}, Question: {question}, Most likely answer: {most_likely_answer}")

if __name__ == "__main__":
    pdf_directory = "./sample_data/"
    questions_path = "questions.txt"
    processor = QuestionProcessor(pdf_directory, questions_path)
    processor.process_questions()
