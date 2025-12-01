from pydantic import BaseModel, EmailStr

class ProfessorLogin(BaseModel):
    email: EmailStr
    senha: str
