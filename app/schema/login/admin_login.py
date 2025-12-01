from pydantic import BaseModel, EmailStr

class AdminLogin(BaseModel):
    email: EmailStr
    senha: str
