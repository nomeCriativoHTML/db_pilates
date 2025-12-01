from pydantic import BaseModel, EmailStr

class AlunoLogin(BaseModel):
    email: EmailStr
    senha: str
