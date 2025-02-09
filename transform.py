from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import requests

# Load model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# Load image
image = Image.open(r"C:\Users\KIRUBA\Desktop\vision related task\images\pic.png")

# Perform OCR
inputs = processor(image, return_tensors="pt")
generated_ids = model.generate(**inputs)
text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(text)
