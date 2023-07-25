from fastapi import APIRouter
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
from services.movie import MovieService
from schemas.movie import Movie

movie_router=APIRouter()


@movie_router.get('/movies',tags=['movies'],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() ->List[Movie]:
    db=Session()
    result=MovieService(db).get_movies()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/{id}',response_model=Movie,status_code=404)
def get_movie(id: int = Path(ge=1,le=200)) -> Movie:
    db=Session()
    result=MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={'message':"No encontrado"})


    return JSONResponse(status_code=200,content=jsonable_encoder(result))
        
@movie_router.get('/movies/',tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category:str =Query(min_length=5,max_length=15)) -> List[Movie]:
    db=Session()
    result=MovieService(db).get_movies_by_category(category)
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@movie_router.post('/movies',tags=['movies'],response_model=dict,status_code=201)
def create_movie(movie:Movie) ->dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201,content={"message":"Se registro la pelicula"})

@movie_router.put("/movies/{id}",tags=["movies"],response_model=dict,status_code=200)
def update_movie(id:int, movie:Movie) -> dict:
    db=Session()
    result=MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={'message':"No se encontró"})
    
    MovieService(db).update_movie(id,movie)
    return JSONResponse(status_code=200,content={'message':"Se ha modificado"})

        
@movie_router.delete("/movies/{id}",tags=["movies"],response_model=dict,status_code=200)
def delete_movie(id:int, movies:Movie) -> dict:
    db=Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404,content={'message':"No se encontró"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200,content={"message":"Se ha eliminado la pelicula"})

