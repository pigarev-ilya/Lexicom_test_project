from pydantic import BaseModel

class WriteData(BaseModel):
    phone: str
    address: str
