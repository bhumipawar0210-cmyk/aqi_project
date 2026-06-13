from pydantic import BaseModel

class UserData(BaseModel):
    name: str
    age: int
    region: str
    asthma: bool
    heart_disease: bool