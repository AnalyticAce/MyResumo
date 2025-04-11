import os
import cv2
import pytesseract
from typing import List, Dict, Any
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image

class OCRVision:
    def __init__(self, pdf_file: str = None, pdf_bytes: bytes = None) -> None:
        self.pdf_file = pdf_file
        self.pdf_bytes = pdf_bytes
        if not pdf_file and not pdf_bytes:
            raise ValueError("Either pdf_file or pdf_bytes must be provided")
            
    def pdf_to_images(self) -> List[Image.Image]:
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
        for path in image_paths:
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error deleting image {path}: {e}")
        return None
    
    @staticmethod
    def ocr_image(image_path: str, lang: str = 'eng') -> str:
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