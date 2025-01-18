from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field, ConfigDict, config 
import numpy as np
from pydantic.dataclasses import dataclass
import easyocr
import cv2

class ArbitraryTypeInput:
    def __init__(self, images):
        self.images = images
        
    def __repr__(self):
        return f'ArbitraryTypeInput(images={self.images!r})'


class ArbitraryTypeoutput:
    def __init__(self, annotated_image):
        self.annotated_image = annotated_image
        
    def __repr__(self):
        return f"ArbitraryTypeoutput(annotated_image={self.annotated_image!r})"
    
    
class imageextractiontoolinput(BaseModel):
    """Input schema for MyCustomTool."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    images: ArbitraryTypeInput = Field(..., description="A list of images represented as numpy arrays.")
    language: List[str] = Field(..., description="A list of language that text extraction support")
    
    
class imageextractiontooloutput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    extracted_text: List[dict]
    annotated_image: ArbitraryTypeoutput
    
class imageextractiontool(BaseTool):
    name: str = "Image Text Extraction Tool"
    description: str = (
        "Extracts text from images using EasyOCR and annotates detected text with bounding boxes."
        )
    args_schema: Type[BaseModel] = imageextractiontoolinput
    return_schema: Type[BaseModel] = imageextractiontooloutput
    
    def _run(self, images: ArbitraryTypeInput, language: List[str]) -> imageextractiontooloutput:
        
        print("language loading...")
        reader = easyocr.Reader(language)
        images = images
        img_values = []
        annotated_image = []
        print('image reading completed')
        for ind, img in enumerate(images):
            H, W, _ = img.shape
            text = reader.readtext(img, paragraph=True)
            img_text = []
            img_text.clear()
            for i in text:
                if len(i) == 3:
                    x, y = int(i[0][0][0]), int(i[0][0][1])
                    w, h = int(i[0][2][0]), int(i[0][2][1])
                    img_text.append({
                        "text" : i[1],
                        'Text_coordinates' : {'bottom_left': (x, y), 'top_right': (w, h)},
                    })
                    cv2.rectangle(img, (x, y), (w, h), (255, 0, 0), 2)
            annotated_image.append(img)
            img_values.append(
                {   
                    f"Image_{ind + 1}": img_text,
                    "Original_image_size(w, h)": (W, H),
                    
                }
            )  
        return imageextractiontooloutput(
            extracted_text=img_values, 
            annotated_image=ArbitraryTypeoutput(annotated_image)
            )


if __name__ == "__main__":
    tool = imageextractiontool()
    img1 = cv2.imread(r"C:\Users\KIRUBA\Downloads\data\data\imgs\vs3_vha_10_0094f_fill.1.png")
    img2 = cv2.imread(r"C:\Users\KIRUBA\Downloads\data\data\imgs\vs3_VBA_21_0960K_2_ARE.3.png")
    img3 = cv2.imread(r"C:\Users\KIRUBA\Downloads\data\data\imgs\vs3_VBA_21P_4718a_ARE.1.png")
    output = tool._run(images=[img1, img2, img3], language=['en'])
    print(output.extracted_text)  
    cv2.imshow("ban", output.annotated_image.annotated_image[0])
    cv2.imshow("ban1", output.annotated_image.annotated_image[1])
    cv2.imshow("ban2", output.annotated_image.annotated_image[2])
    cv2.waitKey(0)
    cv2.destroyAllWindows()