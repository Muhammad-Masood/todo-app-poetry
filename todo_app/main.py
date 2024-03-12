from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.connection import perform_migration
from database.models import Todo

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    perform_migration()
    yield

app = FastAPI(lifespan=lifespan, title="Todo App")


@app.get('/')
def home():
    return {"message": "Todo App","about":"This is a Todo App which is built using python poetry, Fast API and Sql Model. Please check out the README for more details."}

@app.post('/todo/post')
def create_todo(todo: Todo):
    pass

@app.get('/todo/{todo_id}')
def get_todo(todo_id):
    pass

@app.patch('/todo/{todo_id}')
def update_todo():
    pass

@app.delete('/todo/{todo_id}')
def delete_todo(todo_id):
    pass

@app.get('/todos')
def get_todos():
    pass
