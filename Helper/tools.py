import PyPDF2, requests, base64, streamlit as st
import random
from .toast_message import TOAST_MESSAGES

@st.cache_resource(show_spinner=False)
def load_lottie(_url):
    try:
        req = requests.get(_url)
        req.raise_for_status()
        return req.json()
    except requests.exceptions.RequestException as e:
        st.error(f'Error: Unable to load Lottie from URL. {str(e)}', icon='🚨')

class ToolKit:
    def __init__(self) -> None:
        pass

    def get_random_toast(self):
        return random.choice(TOAST_MESSAGES)

    @staticmethod
    def get_file_data(file):
        with open(file, 'rb') as f:
            data = f.read()
        return data

    @staticmethod
    def pdf_to_text(file):
        with open(file, "rb") as pdf:
            reader = PyPDF2.PdfReader(pdf, strict=False)
            pdf_text = []
            for page in reader.pages:
                content = page.extract_text()
                pdf_text.append(content)
            return '  '.join(pdf_text)

    @staticmethod
    def read_file(file):
        with open(file, "r") as f:
            return f.read()

    def create_prompt(self, filename):
        prompt = self.read_file(filename)
        template = f"""
            {prompt}
            """
        return template

    @staticmethod
    def get_pdf_download_link(pdf_path, name):
        with open(pdf_path, 'rb') as f:
            pdf_file = f.read()
        b64 = base64.b64encode(pdf_file).decode()
        href = f'<a href="data:file/pdf;base64,{b64}" download="{name}.pdf">Click here to download your receipe PDF file</a>'
        return href