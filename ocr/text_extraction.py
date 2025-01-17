import easyocr
import streamlit as st
import numpy as np
import cv2
st.title("Text Extraction from Image")


"""
Note:

File extension support: png, jpg, tiff.
File size limit: 2 Mb
Image dimension limit: 1500 pixel
Possible Language Code Combination: Languages sharing the same written script (e.g. latin) can be used together. English can be used with any language.

"""

with st.sidebar:
    
    Language = st.text_input("Enter the Language")
    images = st.file_uploader(
        label="Select all the image you want...",
        type= ['.jpeg', '.png', '.jpg'], 
        accept_multiple_files= True
        )
    if len(Language) <= 0:
        raise ValueError(f"Please Enter the Language...")
    
    if len(images) > 0:
        
        coloured_images = []
        for image in images:
            byte_image = image.getvalue()
            convert_bytes_to_array = np.frombuffer(byte_image, np.uint8)
            RGB_image = cv2.imdecode(convert_bytes_to_array, cv2.IMREAD_COLOR)
            BGR_image = cv2.cvtColor(RGB_image, cv2.COLOR_RGB2BGR)
            height, width = BGR_image.shape[:2]
            if width >= 3000 and height >= 2000:
               resize_image = cv2.resize(BGR_image, (0, 0), fx=0.5, fy=0.5)
               coloured_images.append(resize_image)
               continue
            coloured_images.append(BGR_image)
            
        
print(Language.split(','))      
for img in coloured_images:
    st.image(img)