from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

# User Model
class User(BaseModel):
    username:str
    password:str
    nombre:str
    apellido:str
    direccion:Optional[str]
    telefono:int
    correo:str
    creacion:datetime=datetime.now()

class UpdateUser(BaseModel):
    username: str = None
    password: str = None
    nombre: str = None
    apellido: str = None
    direccion: str = None
    telefono: int = None
    correo: str = None
    creacion: datetime = None

 
class showUser(BaseModel):
    username:str 
    nombre:str
    apellido:str
    correo:str
    class Config():
        from_attributes = True

class Login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None            