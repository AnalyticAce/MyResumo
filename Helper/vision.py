from pdf2image import convert_from_path
import cv2, os, pytesseract
from typing import List
from PIL import Image

class Vision:
    def __init__(self, pdf_file : str) -> None:
        self.pdf_file = pdf_file
        pass

    def pdf_to_image(self) -> List[Image.Image]:
        """ Converts a PDF file to a list of images.

        Returns:
            List[Image.Image]: A list of PIL Image objects.
        """
        images = convert_from_path(self.pdf_file)
        return images

    @staticmethod
    def save_images(images: List[Image.Image], filename: str) -> List[Image.Image]:
        """
        Saves a list of images as JPEG files with modified filenames.

        Parameters
        ----------
            images (List[Image.Image]): A list of PIL Image objects.
            filename (str): The base filename (without extension) for saving images.

        Returns
        -------
            List[str]: A list of saved image filenames.
        """
        save_images_name = []
        for i, img in enumerate(images):
            main = filename.replace('.pdf', "").replace(" ", "_")
            img.save(f'{main}_page{i}.jpg', 'JPEG')
            save_images_name.append(f'{main}_page{i}.jpg')
        return save_images_name

    @staticmethod
    def delete_image(images: List[Image.Image]) -> None:
        """ Deletes a list of images.

        Parameters:
        -----------
            images (List[Image.Image]): A list of PIL Image objects.

        Returns
        -------
            _type_: None
        """
        for i in images:
            os.remove(i)
        return None

    @staticmethod
    def ocr_image(images: List[Image.Image]) -> List[str]:
        """ Extracts text from a list of images using OCR.

        Args:
            images (List[Image.Image]): _description_

        Returns:
            List[str]: _description_
        """
        texts = []
        for image in images:
            text = pytesseract.image_to_string(cv2.imread(image))
            texts.append(text)
        return texts