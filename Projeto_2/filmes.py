from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Filme:
    "Classe filme"
    id: int
    titulo: str
    descricao: str
    genero: str
    avaliacao: int
    data_lancamento: int


    def __init__(self, id, titulo, descricao, genero, avaliacao, data_lancamento):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.genero = genero
        self.avaliacao = avaliacao
        self.data_lancamento = data_lancamento


class FilmeRequest(BaseModel):
    "Validação de dados"
    id: int | None = None
    titulo: str = Field(min_length=3)
    descricao: str = Field(min_length=1, max_length=100)
    genero: str = Field(min_length=1, max_length=50)
    avaliacao: int = Field(gt=-1, lt=11)
    data_lancamento: int = Field(gt=1900, lt=2099)


    class Config:
        "Exemplo do esquema"
        json_schema_extra = {
            'example':{
                'titulo': 'Um filme',
                'descricao': 'Descrição do filme',
                'genero': 'um gênero',
                'avaliacao': 0,
                'data_lancamento': 1900
            }
        }


FILMES = [
    Filme(1, 'Titulo Um', 'Descrição Um', 'Genero Um', 1, 1999),
    Filme(2, 'Titulo Dois', 'Descrição Dois', 'Genero Dois', 3, 2010),
    Filme(3, 'Titulo Tres', 'Descrição Tres', 'Genero Tres', 6, 2023),
    Filme(4, 'Titulo Quatro', 'Descrição Quatro', 'Genero Quatro', 10, 2015),
    Filme(5, 'Titulo Cinco', 'Descrição Cinco', 'Genero Cinco', 5, 1980)
]


@app.get("/filmes/", status_code=status.HTTP_200_OK)
async def mostrar_filmes():
    "Mostra todos os filmes cadastrados."
    return FILMES


@app.get("/filmes/{filme_id}", status_code=status.HTTP_200_OK)
async def mostrar_filme_por_id(filme_id: int):
    "Procura o filme pelo id."
    for filme in FILMES:
        if filme.id == filme_id:
            return filme
    raise http_exception()


@app.post("/filmes/novo_filme/", status_code=status.HTTP_201_CREATED)
async def novo_filme(filme_request: FilmeRequest):
    "Cadastra um novo filme."
    novo_filme = Filme(**filme_request.model_dump())
    FILMES.append(procura_filme_por_id(novo_filme))


@app.put("/filmes/atualizar_filme", status_code=status.HTTP_204_NO_CONTENT)
async def atualizar_filme(filme: FilmeRequest):
    "Atualiza um filme já cadastrado."
    atualizou = False

    for i in enumerate(FILMES):
        if FILMES[i].id == filme.id:
            FILMES[i] = filme
            atualizou = True
    if not atualizou:
        raise http_exception()



def procura_filme_por_id(filme: Filme):
    "Busca o último id e soma +1 para o próximo filme."
    if len(FILMES) > 0:
        filme.id = FILMES[-1].id + 1
    else:
        filme.id = 1
    return filme


def http_exception():
    "Exceção se não encontrar o filme."
    return HTTPException(status_code=404, detail='Filme não encontrado.')
