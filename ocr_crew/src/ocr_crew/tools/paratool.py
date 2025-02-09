from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import easyocr as ocr

class para_tool_input(BaseModel):
    """Input schema for MyCustomTool."""
    path: str = Field(..., description="File path of the image")
    language: str = Field(..., description="Language that present in image for model identification")

class para_tool(BaseTool):
    name: str = "para text extraction"
    description: str = (
        "Used to extract text from the given file path image"
    )
    args_schema: Type[BaseModel] = para_tool_input

    def _run(self, path: str, language: str) -> str:
        languages = language.split(" ")
        reader = ocr.Reader(languages)
        texts = reader.readtext(path, paragraph=False)
        
        if texts:
            para = []
            for text in texts:
                if len(text) == 3:
                    para.append(text[1])
                else:
                    raise ValueError(f"Check the text length")
            return para
        else:
            ValueError(f'no text found in image')
            
if __name__ == "__main__":
    tool = para_tool()
    result = tool._run(path=r"C:\Users\KIRUBA\Desktop\vision related task\images\pic.png", language='en')
    print(result)