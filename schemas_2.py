import typing
from pydantic import BaseModel
import datetime 

class OCRoutput(BaseModel):
    image_origin:str
    fields : OCRextraction_fields





class OCRextraction_fields(BaseModel):
    Name:str
    Date_of_Birth:datetime
    Address:str
    id_no:str
    



