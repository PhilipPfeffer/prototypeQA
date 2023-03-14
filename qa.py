import os
from PyPDF2 import PdfReader
import openai
import env  # This is a file that contains the OpenAI API key
from collections import defaultdict

# Load your OpenAI API key
openai.api_key = env.OPENAI_API_KEY
TEXT_CHUNK_LEN = 1000

# 1. Read questions from .txt file
with open("questions.txt", "r") as file:
    questions = [line.strip() for line in file.readlines()]

# 2. Loop over a directory of .pdf files
pdf_directory = "./sample_data/"

for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith(".pdf"):
        # 3. Read the PDF file
        pdf_path = os.path.join(pdf_directory, pdf_file)
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)

            # 4. Convert the full PDF to text
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()

        all_answers = defaultdict(list)
        for question in questions:
            # 5. Process the text in chunks
            for i in range(0, len(full_text), TEXT_CHUNK_LEN):
                chunk = full_text[i:i + TEXT_CHUNK_LEN]
                prompt = f"Given the following text, give a direct answer with no explanation:\n\n{chunk}\n\nQuestion: {question}\n\nAnswer (reply 'NONE' if the text does not contain the answer):"
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt},
                    ]
                )

                answer = response["choices"][0]["message"]["content"].strip()

                if answer != "NONE" and answer != "'NONE'":
                    all_answers[question].append(answer)

            # 7. Find the most likely answer for each question
            potential_answers = ', '.join(all_answers[question])
            prompt = f"Here are potential answers to the question '{question}', which is most likely to be correct given frequency of appearance? Potential answers: {potential_answers}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )

            most_likely_answer = response["choices"][0]["message"]["content"].strip()
            print(f"File: {pdf_file}, Question: {question}, Most likely answer: {most_likely_answer}")