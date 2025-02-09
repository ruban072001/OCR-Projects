from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from paddleocr import PaddleOCR

class paddle_tool_input(BaseModel):
    """Input schema for MyCustomTool."""
    path: str = Field(..., description="File path of the image")
    language: str = Field(..., description="Language that present in image for model identification")

class paddle_tool(BaseTool):
    name: str = "pad Text extraction"
    description: str = (
        "Used to extract text from the given file path image"
    )
    args_schema: Type[BaseModel] = paddle_tool_input

    def _run(self, path: str, language: str) -> str:

        ocr = PaddleOCR(lang = language)
        result = ocr.ocr(path)
        
        texts = []
        for i in range(len(result[0])):
            texts.append(result[0][i][1][0])
            
        return texts
            
if __name__ == "__main__":
    tool = paddle_tool()
    result = tool._run(path=r"C:\Users\KIRUBA\Desktop\vision related task\images\pic.png", language='en')
    print(result)