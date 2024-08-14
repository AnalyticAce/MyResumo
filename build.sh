#!/bin/bash

# Install the necessary packages
pip install -r requirements.txt
pip install openai==0.28
pip install pytesseract==0.3.10

# Download the English trained data for Tesseract
wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

# Move the trained data to the tessdata directory
# Replace '/usr/local/share/tessdata' with the path to your tessdata directory
mv eng.traineddata /usr/local/share/tessdata

# Add Tesseract to the system's PATH
# Replace '/usr/local/bin' with the path to your Tesseract executable
export PATH=$PATH:/usr/local/bin
