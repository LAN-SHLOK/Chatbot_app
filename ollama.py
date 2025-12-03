from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv


load_dotenv()

# langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

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