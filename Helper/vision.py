from pdf2image import convert_from_path
import cv2
import os
import pytesseract

def pdf_to_image(pdf_file):
    images = convert_from_path(pdf_file)
    return images

def save_images(images, filename):
    save_images_name = []
    for i in range(len(images)):
        main = filename.replace('.pdf', "").replace(" ", "_")
        images[i].save(f'{main}_page'+ str(i) +'.jpg', 'JPEG')
        save_images_name.append(f'{main}_page'+ str(i) +'.jpg')
    return save_images_name

def delete_image(images):
    for i in images:
        os.remove(i)
    return None

def ocr_image(images):
    texts = []
    for image in images:
        text = pytesseract.image_to_string(cv2.imread(image))
        texts.append(text)
    return texts