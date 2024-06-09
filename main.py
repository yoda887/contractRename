# pip install ollama
# pip install langchain
# pip install pymupdf

# import ollama
#
# response = ollama.generate(model='phi',
#                            prompt='what is a qubit?')
# print(response['response'])

# import fitz  # PyMuPDF
import ollama
import PyPDF2

import os
import ollama
from groq import Groq

os.environ["GROQ_API_KEY"] = "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"
# os.environ["GROQ_API_KEY"] = "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"

def extract_text_from_pdf(pdf_path):
    document = PyPDF2.PdfReader(pdf_path)
    text = ""

    # get number of pages
    NumPages = len(document.pages)

    # extract text from each page
    # for i in range(NumPages):
    #     PageObj = document.pages[i]
    #     page = PageObj.extract_text()
    #     text += page

    PageObj = document.pages[0]
    page = PageObj.extract_text()
    text = page

    return text


def extract_information_from_text(text):
     # Create the prompt for the ollama model
    # prompt = f"Extract the parties involved and the contract number from the following text:\n\n{text} " \
    #          f"in next format 'name of supplyer number of contract name and number of annex'"

    prompt = f"Extract the parties involved and the contract number from the following text:\n\n{text}\n\n"\
         "Provide the information in the format: 'Name of Supplier, Number of Contract, Name of Annex, Number of Annex'."


    # Generate the response using ollama
    response = ollama.generate(model='phi3:latest', prompt=prompt)
    return response['response']


def query_summaries(text):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    prompt = f"From the following text:\n\n{text}\n\n" \
             "Provide the information in one string line, uncapitla chars in the format: 'Name of Supplier, Number of Contract, Name of Annex, Number of " \
             "Annex' - as name of file. Just name of file and thats all. Only file name. In ukrainian. " \
             "Only name of company - without ТОВ, АТ etc. Remove all dots and commas. Print only name of file. Dont print - Here is the file name"


    prompt = prompt.strip()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-70b-8192",
    )

    summaries = chat_completion.choices[0].message.content

    return summaries

def main():
    pdf_path = "C:\\Google Drive\\fr1\\додатки 201600650001.pdf"  # Replace with the path to your PDF file
    pdf_text = extract_text_from_pdf(pdf_path)
    # extracted_information = extract_information_from_text(pdf_text)
    extracted_information = query_summaries(pdf_text)
    print(extracted_information)


if __name__ == "__main__":
    main()
