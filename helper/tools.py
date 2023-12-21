import streamlit as st
import base64
from PIL import Image
import PyPDF2
import requests

def load_lottie(url): 
    req = requests.get(url)
    if req.status_code != 200:
        None
    return req.json()

def get_file_data(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data

def pdf_to_text(file):
    
    with open(file, "rb") as pdf:
        reader = PyPDF2.PdfFileReader(pdf, strict=False)
        
        pdf_text = []
        
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
            
        return pdf_text