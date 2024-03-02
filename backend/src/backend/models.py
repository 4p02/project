"""FastAPI route parameter data models. Not database table models!"""

from pydantic import BaseModel


class Register(BaseModel):
    password: str
    email: str
    full_name: str

class Login(BaseModel):
    password: str
    email: str


class Summarize(BaseModel):
    url: str
