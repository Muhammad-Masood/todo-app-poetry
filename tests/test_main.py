from fastapi.testclient import TestClient
from sqlmodel import Field, Session, SQLModel, create_engine, select
from database.models import Todo
from main import app, get_session
from dotenv import load_dotenv
import os
from fastapi import HTTPException, Depends
from typing import Annotated

_:bool = load_dotenv()

connection_string = str(os.getenv("TEST_CONNECTION_STRING")).replace(
    "postgresql", "postgresql+psycopg2")

engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
SQLModel.metadata.create_all(engine)

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

client = TestClient(app=app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Todo App"

def test_create_todo():
    todo = Todo(title="Test Todo", description="This is a test todo")
    response = client.post("/todo/post", data=todo.model_dump_json())
    response_data = response.json()
    session = next(get_test_session())
    created_todo = session.exec(select(Todo).where(Todo.id == response_data.get("id"))).first()
    assert response.status_code == 200
    assert response_data == created_todo.model_dump()

def test_get_todo():
    todo = Todo(title="Test Todo 2", description="This is a test todo 2")
    created_todo = client.post("/todo/post", data=todo.model_dump_json())
    created_todo_data = created_todo.json()
    created_todo_id = created_todo_data.get("id")
    response = client.get(f"/todo/{created_todo_id}")
    assert response.status_code == 200
    assert response.json() == created_todo_data

def test_get_non_existent_todo():
    response = client.get("/todo/123")
    assert response.status_code == 404

def get_todos():
    response = client.get("/todos")
    todos = response.json()
    assert response.status_code == 200
    assert todos.__len__() > 0

def test_update_todo():
    todo = Todo(title="Test Todo 3", description="This is a test todo 3")
    response = client.post("/todo/post", data=todo.model_dump_json())
    created_todo_id = response.json().get("id")
    updated_todo = Todo(title="Updated Test Todo 3", description="This is an updated test todo 3")
    response = client.patch(f"/todo/{created_todo_id}", data=updated_todo.model_dump_json())
    updated_todo_response_data = client.get(f"/todo/{created_todo_id}").json()
    assert response.status_code == 200
    assert response.json().message == "Todo updated successfully"
    assert updated_todo_response_data == updated_todo.model_dump()

# def test_update_non_existent_todo():
#     new_todo = Todo(title="Updated Non Existent Todo",description="This is an updated non existent todo")
#     response = client.patch("/todo/123", data=new_todo.model_dump_json())
#     print(response)
#     print(response.json())
#     assert response.status_code == 404

def test_delete_todo():
    todo = Todo(title="Test Todo 4", description="This is a test todo 4")
    response = client.post("/todo/post", data=todo.model_dump_json())
    todos_len_db = client.get("/todos").json().__len__()
    created_todo_id = response.json().get("id")
    response = client.delete(f"/todo/{created_todo_id}")
    expected_response_message = "Todo deleted successfully"
    assert response.status_code == 200
    assert response.json().get("message") == expected_response_message
    todos_len_after_delete = client.get("/todos").json().__len__()
    assert todos_len_db > todos_len_after_delete
    response = client.get(f"/todo/{created_todo_id}")
    assert response.status_code == 404