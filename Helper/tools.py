import streamlit as st
import PyPDF2
import requests
import base64

@st.cache_resource(show_spinner=False)
def load_lottie(url): 
    try:
        req = requests.get(url)
        req.raise_for_status()
        return req.json()
    except requests.exceptions.RequestException as e:
        st.error(f'Error: Unable to load Lottie from URL. {str(e)}', icon='🚨')

@st.cache_resource(show_spinner=False)
def get_file_data(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data

@st.cache_resource(show_spinner=False)
def pdf_to_text(file):
    with open(file, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
        return '  '.join(pdf_text)

@st.cache_resource(show_spinner=False)
def read_file(file):
    with open(file, "r") as f:
        return f.read()

@st.cache_resource(show_spinner=False)
def create_prompt(filename):
    prompt = read_file(filename)
    template = f"""
        {prompt}
        """
    return template

@st.cache_resource(show_spinner=False)
def extract_json(text):
	start = text.find("{")
	end = text.rfind("}") + 1
	return text[start:end]

def get_pdf_download_link(pdf_path, name):
    with open(pdf_path, 'rb') as f:
        pdf_file = f.read()
    b64 = base64.b64encode(pdf_file).decode()
    href = f'<a href="data:file/pdf;base64,{b64}" download="{name}.pdf">Click here to download your receipe PDF file</a>'
    return href