import easyocr

reader = easyocr.Reader(['en'])

# to read words in image
words = reader.readtext(r"C:\Users\KIRUBA\Desktop\vision related task\images\para img.jpg")
print(words)
# to read a paragraph in a images

para = reader.readtext(r"C:\Users\KIRUBA\Desktop\vision related task\images\para img.jpg", paragraph=True)
print(para)