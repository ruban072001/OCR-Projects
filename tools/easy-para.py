from pydantic import BaseModel, ConfigDict, Field
from crewai.tools import BaseTool
from typing import List, Type
import easyocr as ocr
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

hug_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")

class easy_tool_input(BaseModel):
    name: str = Field(..., description = "Name of the Image")

class easy_ocr_tool(BaseTool):
    name: str = "EasyTool"
    description: str = (
        "Used to extract texts from images"
    )
    args_schema: Type[BaseModel] = easy_tool_input
    model_config = ConfigDict(extra="allow")
    
    def __init__(self, language: List[str], file_path: str, img_name: str):
        super().__init__()
        self.language = language
        self.file_path = file_path
        self.img_name = img_name
        self.reader = ocr.Reader(self.language)
        self.storing_image_to_db()
        
    def extract_text_from_image(self):
        texts = self.reader.readtext(self.file_path, paragraph=True)
        
        if texts:
            para = []
            for text in texts:
                if len(text) == 2:
                    para.append(text[1])
                else:
                    raise ValueError(f"Check the text length")
            return para
        else:
            ValueError(f'no text found in image')
        
    def create_db(self):
        
        self.current = os.path.dirname(__file__)
        self.db_name = os.path.join(self.current, "TS_DB")
        if not os.path.exists(self.db_name):
            os.mkdir(self.db_name)
            
        self.db_path = os.path.join(self.db_name, "image_collections")
        if not os.path.exists(self.db_path):
            os.mkdir(self.db_path)
                 
    def storing_image_to_db(self):
        
        self.create_db()
        paras = self.extract_text_from_image()
        
        metadatas = [{'source': self.img_name} for i in range(len(paras))]
        faiss_db = FAISS.from_texts(paras, embedding=hug_model, metadatas=metadatas)
        faiss_db.save_local(self.db_path)
    
    
    def _run(self, name: str):
        self.create_db()
        load_db = FAISS.load_local(self.db_path, embeddings=hug_model, allow_dangerous_deserialization=True)
        context = load_db.as_retriever(search_kwargs={'filter': {'source':name}})
        return context
    
if __name__ == "__main__":
    tool = easy_ocr_tool(
        language=['en'],
        file_path=r"C:\Users\KIRUBA\Desktop\vision related task\images\pic.png",
        img_name="image-1"
    )
    result = tool._run("image-1")
    print(result)