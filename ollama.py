from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv


load_dotenv()

prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that translates English to French."),
        ("user", "Question: {question}"),
    ]
)

st.title("Simple LangChain LLama2 Chat App")
input_text = st.text_input("Enter your question here:")

# openai llm call

llm = Ollama(model="llama2")
Output_parser=StrOutputParser()

# chain
chain=prompt | llm | Output_parser  

if input_text:

    st.write(chain.invoke({"question": input_text}))
