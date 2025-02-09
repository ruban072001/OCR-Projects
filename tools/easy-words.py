from pydantic import BaseModel, ConfigDict, Field
from crewai.tools import BaseTool
from typing import List, Type
import easyocr as ocr


class easy_tool_input(BaseModel):
    file_path: str = Field(..., description = "File path for Image")

class easy_ocr_tool(BaseTool):
    name: str = "EasyTool"
    description: str = (
        "Used to extract texts from images"
    )
    args_schema: Type[BaseModel] = easy_tool_input
    model_config = ConfigDict(extra="allow")
    
    def __init__(self, language: List[str]):
        super().__init__()
        self.language = language

        self.reader = ocr.Reader(self.language)
    
    def _run(self, file_path: str):
        texts = self.reader.readtext(file_path, paragraph=False)
        
        words = []
        for text in texts:
            if len(text) == 3:
                words.append(text[1])
            else:
                raise ValueError(f"Check the text length")
        return words
    
    
if __name__ == "__main__":
    tool = easy_ocr_tool(
        language=['en']
    )
    result = tool._run(r"C:\Users\KIRUBA\Desktop\vision related task\images\pic.png")
    print(result)