from fastapi import FastAPI, Body

app = FastAPI()

LIVROS = [
    {'titulo': 'Titulo Um', 'autor': 'Autor Um', 'categoria': 'ciencia'},
    {'titulo': 'Titulo Dois', 'autor': 'Autor Dois', 'categoria': 'historia'},
    {'titulo': 'Titulo Tres', 'autor': 'Autor Tres', 'categoria': 'programacao'},
    {'titulo': 'Titulo Quatro', 'autor': 'Autor Quatro', 'categoria': 'matematica'},
    {'titulo': 'Titulo Cinco', 'autor': 'Autor Tres', 'categoria': 'ciencia'},
    {'titulo': 'Titulo Seis', 'autor': 'Autor Dois', 'categoria': 'ingles'}
]


@app.get("/livros")
async def mostrar_livros():
    "Mostra todos os livros, com autor e categoria."
    return LIVROS


@app.get("/livros/{livro_titulo}")
async def mostrar_por_titulo(livro_titulo: str):
    "Busca o livro pelo título."
    for livro in LIVROS:
        if livro.get('titulo').casefold() == livro_titulo.casefold():
            return livro


@app.get("/livros/")
async def mostrar_por_categoria(categoria: str):
    "Busca o livro pela categoria."
    retornar_livros = []
    for livro in LIVROS:
        if livro.get('categoria').casefold() == categoria.casefold():
            retornar_livros.append(livro)
    return retornar_livros


@app.get("/livros/{livro_autor}/")
async def mostrar_por_autor_e_categoria(livro_autor: str, categoria: str):
    "Busca livre pelo autor e pela categoria."
    retornar_livros = []
    for livro in LIVROS:
        if livro.get('autor').casefold() == livro_autor.casefold() and livro.get('categoria').casefold() == categoria.casefold():
            retornar_livros.append(livro)
    return retornar_livros


@app.post("/livros/adicionar_livro")
async def adicionar_livro(novo_livro=Body()):
    "Adiciona um novo livro pelo docs."
    LIVROS.append(novo_livro)


@app.put("/livros/atualizar_livro")
async def atualizar_livro(atualizar_livro=Body()):
    "Atualiza um livro pelo docs."
    for i in range(len(LIVROS)):
        if LIVROS[i].get('titulo').casefold() == atualizar_livro.get('titulo').casefold():
            LIVROS[i] = atualizar_livro
            
            
@app.delete("/livros/deletar_livro/{livro_titulo}")
async def deletar_livro(livro_titulo: str):
    "Deleta um livro pelo título."
    for i in range(len(LIVROS)):
        if LIVROS[i].get('titulo').casefold() == livro_titulo.casefold():
            LIVROS.pop(i)
            break
        
@app.get("/livros/autor/{pesquisa}")
async def pesquisar_por_autor(livro_autor: str):
    "Esse é um desafio do professor, fiz uma pesquisa do livro pelo autor."
    lista_pesquisa = []
    for livro in LIVROS:
        if livro.get("autor").casefold() == livro_autor.casefold():
            lista_pesquisa.append(livro)
    return lista_pesquisa