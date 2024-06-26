import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

# Configure the generative AI model
genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def send_message(prompt):
    response = model.start_chat(history=[]).send_message(prompt,)
    return response.text

def code_completion(content):
    prompt = "Complete the code:\n" + content
    completion = send_message(prompt)
    st.write("Code Completion")
    st.markdown(completion)

def debugging_assistant(content):
    prompt = "Debug the code:\n" + content
    debug = send_message(prompt)
    st.write("Debugging")
    st.markdown(debug)

def document_retrieval(function_name):
    prompt = "Retrieve documentation for:\n" + function_name
    retrieval = send_message(prompt)
    st.write("Documentation")
    st.markdown(retrieval)

def code_generation(description):
    prompt = "Generate code to:\n" + description
    generated_code = send_message(prompt)
    st.write("Generatede Code")
    st.markdown(generated_code)


st.title("Codding AI Assistant")

st.sidebar.title("Options")
option = st.sidebar.selectbox("Choose an option", ("Code Generation", "Code Completion", "Debugging Assistant", "Document Retrieval"))

if option == "Code Completion":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", value=content, height=300)
        if st.button("Complete Code"):
            code_completion(content)

elif option == "Debugging Assistant":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", value=content, height=300)
        if st.button("Debug Code"):
            debugging_assistant(content)

elif option == "Document Retrieval":
    function_name = st.text_input("Enter function name or library")
    if st.button("Retrieve Documentation"):
        document_retrieval(function_name)

elif option == "Code Generation":
    description = st.text_input("Enter description of the task")
    if st.button("Generate Code"):
        code_generation(description)
