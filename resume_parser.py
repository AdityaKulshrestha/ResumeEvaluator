from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from pypdf import PdfReader
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
import os
import streamlit as st
from streamlit_chat import message


st.title("Smart AI Resume Evaluator")


openai_key = st.text_input("Enter your OpenAI key", type='password')
os.environ['OPENAI_API_KEY'] = openai_key

resume = st.file_uploader("Upload your resume", type="PDF")
job_description = st.text_input("Enter the description of the job.")


def feedback(resume, job, query):
    with open('prompt.txt', 'r') as f:
        template = f.read()
    prompt = PromptTemplate(
        input_variables=["resume", "job_description", 'query'],
        template=template,
    )
    with get_openai_callback() as cb:
        chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=prompt)
        return chain.run({'resume': resume, 'job_description': job, "query": query})


if resume is not None:
    reader = PdfReader(resume)
    number_of_pages = len(reader.pages)
    text = ""
    for pg in range(number_of_pages):
        page = reader.pages[pg]
        extracted_text = page.extract_text()
        text += extracted_text

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'messages' not in st.session_state:
    st.session_state.messages = []


def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


user_input = get_text()

if st.button("Submit", key='Final_submit') and user_input:
    output = feedback(resume, job_description, user_input)
    print(type(output))
    print(output)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    print(st.session_state)

    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


