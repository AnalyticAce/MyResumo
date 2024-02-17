import streamlit as st
import base64
from PIL import Image
import PyPDF2
import requests
import os

@st.cache_data(show_spinner=False)
def load_lottie(url): 
    try:
        req = requests.get(url)
        req.raise_for_status()
        return req.json()
    except requests.exceptions.RequestException as e:
        st.error(f'Error: Unable to load Lottie from URL. {str(e)}', icon='🚨')

@st.cache_data(show_spinner=False)
def get_file_data(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data

@st.cache_data(show_spinner=False)
def pdf_to_text(file):
    with open(file, "rb") as pdf:
        reader = PyPDF2.PdfFileReader(pdf, strict=False)
        
        pdf_text = []
        
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
            
        return pdf_text