from pydantic import BaseModel


class Register(BaseModel):
    password: str
    email: str
    full_name: str

class Login(BaseModel):
    password: str
    email: str


class Summerize(BaseModel):
    url: str


