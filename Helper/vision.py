from pdf2image import convert_from_path
import cv2, os, pytesseract

class Vision:
    def __init__(self, pdf_file) -> None:
        self.pdf_file = pdf_file
        pass

    def pdf_to_image(self):
        images = convert_from_path(self.pdf_file)
        return images

    @staticmethod
    def save_images(images, filename):
        save_images_name = []
        for i in range(len(images)):
            main = filename.replace('.pdf', "").replace(" ", "_")
            images[i].save(f'{main}_page'+ str(i) +'.jpg', 'JPEG')
            save_images_name.append(f'{main}_page'+ str(i) +'.jpg')
        return save_images_name

    @staticmethod
    def delete_image(images):
        for i in images:
            os.remove(i)
        return None

    @staticmethod
    def ocr_image(images):
        texts = []
        for image in images:
            text = pytesseract.image_to_string(cv2.imread(image))
            texts.append(text)
        return texts