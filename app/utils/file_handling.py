import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional
import PyPDF2
import pytesseract
from pdf2image import convert_from_path


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.
    
    This function attempts to extract text in two ways:
    1. Direct text extraction using PyPDF2
    2. OCR using pytesseract if direct extraction doesn't yield enough text
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        str: Extracted text content
    """
    # Try direct extraction first
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n\n"

        # If we got a reasonable amount of text, return it
        if len(text.strip()) > 100:
            return text
    except Exception as e:
        print(f"Direct PDF text extraction failed: {e}")
        text = ""

    # If direct extraction failed or didn't get enough text, try OCR
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        
        # Perform OCR on each image
        ocr_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            ocr_text += text + "\n\n"
            
        return ocr_text
    except Exception as e:
        print(f"OCR extraction failed: {e}")
        # If OCR fails but we have some text from direct extraction, use that
        if text:
            return text
        return f"Text extraction failed. Error: {str(e)}"


def save_pdf_file(content: bytes, filename: str, directory: str) -> str:
    """
    Save PDF content to a file in the specified directory.
    
    Args:
        content: PDF file content as bytes
        filename: Name for the saved file
        directory: Directory to save the file in
        
    Returns:
        str: Path to the saved file
    """
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Create file path
    file_path = os.path.join(directory, filename)
    
    # Write content to file
    with open(file_path, 'wb') as file:
        file.write(content)
    
    return file_path


def create_temporary_pdf(latex_content: str) -> Optional[str]:
    """
    Generate a PDF from LaTeX content.
    
    Args:
        latex_content: LaTeX source code
        
    Returns:
        Optional[str]: Path to the generated PDF file, or None if generation fails
    """
    # Create a temporary directory for LaTeX compilation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write LaTeX content to a temporary file
        tex_path = Path(temp_dir) / "resume.tex"
        with open(tex_path, "w", encoding="utf-8") as tex_file:
            tex_file.write(latex_content)
        
        # Compile LaTeX to PDF
        try:
            # Run pdflatex twice to ensure references are resolved
            for _ in range(2):
                process = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", tex_path.name],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=30  # 30 seconds timeout
                )
            
            # Check if PDF was created
            pdf_path = Path(temp_dir) / "resume.pdf"
            if not pdf_path.exists():
                print(f"PDF generation failed: {process.stderr}")
                return None
            
            # Copy the PDF to a location that will persist after the temp directory is deleted
            permanent_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            permanent_pdf.close()
            
            with open(pdf_path, "rb") as src_file:
                with open(permanent_pdf.name, "wb") as dest_file:
                    dest_file.write(src_file.read())
            
            return permanent_pdf.name
            
        except subprocess.TimeoutExpired:
            print("PDF generation timed out")
            return None
        except Exception as e:
            print(f"PDF generation failed: {str(e)}")
            return None