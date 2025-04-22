"""OCR vision processing utilities for document extraction.

This module provides functionality for extracting text from PDF documents using
Optical Character Recognition (OCR). It includes utilities for converting PDFs to
images, processing those images, and extracting structured text content.
"""

import os
from typing import List

import cv2
import pytesseract
from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image


class OCRVision:
    """OCR utility class for extracting text from PDF documents.
    
    This class provides functionality to convert PDF files to images and
    extract text content using Optical Character Recognition (OCR).
    
    Attributes:
    ----------
        pdf_file (str): Path to the PDF file to process.
        pdf_bytes (bytes): Raw bytes of a PDF file to process.
    """
    
    def __init__(self, pdf_file: str = None, pdf_bytes: bytes = None) -> None:
        """Initialize the OCR Vision processor with either a file path or bytes.
        
        Args:
            pdf_file (str, optional): Path to the PDF file to process. Defaults to None.
            pdf_bytes (bytes, optional): Raw bytes of a PDF file. Defaults to None.
            
        Raises:
        ------
            ValueError: If neither pdf_file nor pdf_bytes is provided.
        """
        self.pdf_file = pdf_file
        self.pdf_bytes = pdf_bytes
        if not pdf_file and not pdf_bytes:
            raise ValueError("Either pdf_file or pdf_bytes must be provided")
            
    def pdf_to_images(self) -> List[Image.Image]:
        """Convert a PDF document to a list of PIL Image objects.
        
        Returns:
        -------
            List[Image.Image]: List of PIL Image objects, one per page of the PDF.
            Returns an empty list if an error occurs during conversion.
            
        Raises:
        ------
            Exception: If an error occurs during PDF conversion. The exception is caught
                       and logged, returning an empty list.
        """
        try:
            if self.pdf_file:
                images = convert_from_path(self.pdf_file)
            else:
                images = convert_from_bytes(self.pdf_bytes)
            print(f"Converted PDF to {len(images)} images")
            return images
        except Exception as e:
            print(f"Error converting PDF to images: {e}")
            return []
    
    @staticmethod
    def save_images(images: List[Image.Image], base_filename: str) -> List[str]:
        """Save a list of PIL Image objects to disk as JPEG files.
        
        Creates a 'temp_images' directory if it doesn't exist and saves all images
        with sequential page numbers based on the provided base filename.
        
        Args:
            images (List[Image.Image]): List of PIL Image objects to save.
            base_filename (str): Base name for the saved image files.
            
        Returns:
        -------
            List[str]: List of file paths for the saved images.
        """
        save_images_name = []
        os.makedirs('temp_images', exist_ok=True)
        for i, img in enumerate(images):
            main = base_filename.replace('.pdf', "").replace(" ", "_")
            filename = f'temp_images/{main}_page{i}.jpg'
            img.save(filename, 'JPEG')
            save_images_name.append(filename)
        return save_images_name
    
    @staticmethod
    def delete_images(image_paths: List[str]) -> None:
        """Delete a list of image files from disk.
        
        Args:
            image_paths (List[str]): List of file paths to delete.
        """
        for path in image_paths:
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error deleting image {path}: {e}")
        return None
    
    @staticmethod
    def ocr_image(image_path: str, lang: str = 'eng') -> str:
        """Perform OCR on a single image file to extract text.
        
        Args:
            image_path (str): Path to the image file to process.
            lang (str, optional): Language code for OCR. Defaults to 'eng'.
            
        Returns:
        -------
            str: Extracted text from the image. 
                Returns an empty string if an error occurs.
        """
        try:
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(thresh, lang=lang, config=custom_config)
            return text
        except Exception as e:
            print(f"Error in OCR for {image_path}: {e}")
            return ""
        
if __name__ == "__main__":
    ocr = OCRVision(pdf_file='../data/resume.pdf')
    images = ocr.pdf_to_images()
    saved_images = ocr.save_images(images, 'resume.pdf')
    
    for image_path in saved_images:
        text = ocr.ocr_image(image_path)
        print(f"OCR result for {image_path}: {text}")
    
    ocr.delete_images(saved_images)