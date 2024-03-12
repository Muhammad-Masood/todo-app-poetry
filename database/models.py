from sqlmodel import Field, SQLModel
from uuid import uuid4, UUID
from typing import Optional

class Todo(SQLModel):
    id: Optional[int] = Field(primary_key=True, default_factory=uuid4)
    title: str = Field(nullable=False)
    description: str
    status: bool = Field(default=False)