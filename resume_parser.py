from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from pypdf import PdfReader
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
import os
import streamlit as st

st.title("Your medical buddy!")

openai_key = st.text_input("Enter your OpenAI key", type='password')

os.environ['OPENAI_API_KEY'] = openai_key


resume = st.file_uploader("Upload your resume", type="PDF")
job_description = st.text_input("Enter the description of the job.")


def feedback(resume, job):
    with open('prompt.txt', 'r') as f:
        template = f.read()
    prompt = PromptTemplate(
        input_variables=["resume", "job_description"],
        template=template,
    )
    with get_openai_callback() as cb:
        chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=prompt)
        return chain.run({'resume': resume, 'job_description': job}), cb


if resume is not None:
    # base64_pdf = base64.b64encode(resume.read()).decode("utf-8")
    # pdf_display = (
    #     f'<embed src="data:application/pdf;base64,{base64_pdf}" '
    #     'width="800" height="1000" type="application/pdf"></embed>'
    # )
    # st.markdown(pdf_display, unsafe_allow_html=True)
    reader = PdfReader(resume)
    number_of_pages = len(reader.pages)
    print(number_of_pages)
    text = ""
    for pg in range(number_of_pages):
        page = reader.pages[pg]
        extracted_text = page.extract_text()
        text += extracted_text
    # st.text(extracted_text)

if st.button("Submit", key='Final_submit'):
    response, tokens = feedback(resume, job_description)
    st.markdown(response)
