from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
import models
from models import Livros
from database import engine, SessionLocal
from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def obter_bd():
    "Obter sessão do banco de dados e garantir que feche o término."
    bd = SessionLocal()
    try:
        yield bd
    finally:
        bd.close()


dependencia_bd = Annotated[Session, Depends(obter_bd)]


class LivroRequest(BaseModel):
    "Validação de dados."
    nome: str = Field(min_length=3)
    autor: str = Field(min_length=3)
    sinopse: str = Field(min_length=0)
    ranking: int = Field(gt=0, lt=6)
    lido: bool = Field(default=False)


@app.get("/", status_code=status.HTTP_200_OK)
async def mostrar_livros(bd: dependencia_bd):
    "Mostra todos os livros cadastrados no banco de dados."
    return bd.query(Livros).all()


@app.get("/livros/{livro_id}", status_code=status.HTTP_200_OK)
async def pesquisar_livro(bd: dependencia_bd, livro_id: int = Path(gt=0)):
    "Procura o livro pelo ID."
    modelo = bd.query(Livros).filter(Livros.id == livro_id).first()
    
    if modelo is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    return modelo


@app.post("/livros/{livro_id}", status_code=status.HTTP_201_CREATED)
async def cadastrar_livro(bd: dependencia_bd, livro_request: LivroRequest):
    "Cadastra um novo livro."
    modelo = Livros(** livro_request.model_dump())
    bd.add(modelo)
    bd.commit()


@app.put("/livros/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def atualizar_livro(bd: dependencia_bd, livro_request: LivroRequest, livro_id: int = Path(gt=0)):
    "Atualiza um livro já cadastrado."
    modelo = bd.query(Livros).filter(Livros.id == livro_id).first()
    
    if modelo is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    modelo.nome = livro_request.nome
    modelo.autor = livro_request.autor
    modelo.sinopse = livro_request.sinopse
    modelo.ranking = livro_request.ranking
    modelo.lido = livro_request.lido
    
    bd.add(modelo)
    bd.commit()
    
    return modelo


@app.delete("/livros/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_livro(bd: dependencia_bd, livro_id: int = Path(gt=0)):
    "Deleta um livro cadastrado."
    modelo = bd.query(Livros).filter(Livros.id == livro_id).first()
    
    if modelo is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    bd.query(Livros).filter(Livros.id == livro_id).delete()
    
    bd.commit()