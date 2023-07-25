from fastapi import FastAPI,Body, Path,Query,HTTPException,Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional,List
from starlette.requests import Request
from jwt_manager import create_token,validate_token
from config.database import Session,engine,Base
from models.movie import MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()

app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id:Optional[int]=None
    title:str = Field(min_length=5,max_length=15)
    overview:str = Field(min_length=15,max_length=50)
    year:int = Field(le=2022)
    rating:float = Field(ge=1,le=10)
    category:str = Field(min_length=5,max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id":1,
                "title":"Mi pelicula",
                "overview": "Descripción de la película",
                "year":2022,
                "rating":9.8,
                "category": "Acción"
            }
        }


movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
        {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get('/',tags=["home"])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')
