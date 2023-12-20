import streamlit as st
import base64
from pdf2image import convert_from_path
from PIL import Image
import PyPDF2

def get_binary_file_downloader_link(file, file_label='File'):
    with open(file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    
    return href

def pdf_to_text(file):
    
    with open(file, "rb") as pdf:
        reader = PyPDF2.PdfFileReader(pdf, strict=False)
        
        pdf_text = []
        
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
            
        return pdf_text