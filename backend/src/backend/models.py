"""FastAPI route parameter data models. Not database table models!"""

from pydantic import BaseModel

# todo: implement some sort of captcha for these
class Register(BaseModel):
    password: str
    email: str
    fullname: str

class Login(BaseModel):
    password: str
    email: str


class Summarize(BaseModel):
    url: str
