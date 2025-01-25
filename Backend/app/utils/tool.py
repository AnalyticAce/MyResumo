import PyPDF2

def get_file_data(file: str) -> bytes:
    with open(file, 'rb') as f:
        data = f.read()
    return data

def pdf_to_text(file: str) -> str:
    with open(file, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
        return '  '.join(pdf_text)

def read_file(file: str) -> str:
    with open(file, "r") as f:
        return f.read()

def create_prompt(filename: str) -> str:
    prompt = read_file(filename)
    template = f"""
        {prompt}
        """
    return template