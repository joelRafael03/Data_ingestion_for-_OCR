from typing import List
from pydantic import BaseModel


class OCRLine(BaseModel):
    text: str
    confidence: float
    bbox: List[int]


class OCRPage(BaseModel):
    image: str
    orientation: int
    ocr_results: List[OCRLine]