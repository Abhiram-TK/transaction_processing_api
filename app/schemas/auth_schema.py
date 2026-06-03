from pydantic import BaseModel, Field


class UserRegister(BaseModel):

    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=4)
    role: str

class UserLogin(BaseModel):

    username: str
    password: str

class TokenResponse(BaseModel):

    access_token: str
    token_type: str