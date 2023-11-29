from fastapi import FastAPI, Body

app = FastAPI()

TAREFAS = [
    {'titulo': 'Titulo Um', 'descricao': 'Descricao Um', 'prioridade': 1, 'data': '10/10/2000', 'horario': '00:00'},
    {'titulo': 'Titulo Dois', 'descricao': 'Descricao Dois', 'prioridade': 5, 'data': '24/11/2010', 'horario': '06:00'},
    {'titulo': 'Titulo Tres', 'descricao': 'Descricao Tres', 'prioridade': 3, 'data': '01/01/1980', 'horario': '09:00'},
    {'titulo': 'Titulo Quatro', 'descricao': 'Descricao Quatro', 'prioridade': 2, 'data': '15/09/2023', 'horario': '10:40'},
    {'titulo': 'Titulo Cinco', 'descricao': 'Descricao Cinco', 'prioridade': 4, 'data': '06/07/2050', 'horario': '12:36'}
]


@app.get("/tarefas/")
async def mostrar_afazeres():
    "Mostra todas as terefas."
    return TAREFAS


@app.get("/tarefa/")
async def mostrar_trarefa(titulo: str):
    "Mostra uma tarefa pelo título."
    lista_tarefas = []
    for tarefa in TAREFAS:
        if tarefa.get('titulo').casefold() == titulo.casefold():
            lista_tarefas.append(tarefa)
    return lista_tarefas


@app.post("/tarefas/nova_tarefa/")
async def nova_tarefa(nova_tarefa=Body()):
    "Cria uma nova tafera."
    TAREFAS.append(nova_tarefa)


@app.put("/tarefas/atualizar_tarefa/")
async def atualizar_tarefa(atualizar_tarefa=Body()):
    "Atualiza uma tarefa."
    for tarefa in TAREFAS:
        if tarefa.get('titulo').casefold() == atualizar_tarefa.get('titulo').casefold():
            tarefa.update(atualizar_tarefa)


@app.delete("/tarefas/deletar")
async def deletar_tarefa(deletar_tarefa: str):
    "Deleta uma tarefa"
    for tarefa in TAREFAS:
        if tarefa.get('titulo').casefold() == deletar_tarefa.casefold():
            TAREFAS.remove(tarefa)
