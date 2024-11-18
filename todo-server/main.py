from typing import Union, List, Annotated, Optional, Dict

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from models import User, Todo
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from collections import defaultdict
from sqlalchemy.orm.attributes import flag_modified



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


# Pydantic Models
class TodoCreate(BaseModel):
    description: str
    tags: Optional[List[str]] = []
    done: Optional[bool] = False


class TodoResponse(BaseModel):
    id: int
    user_id: int
    description: str
    tags: List[str]
    done: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    invited_todo_ids: Optional[List[int]] = []

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    invited_todo_ids: List[int]

    class Config:
        orm_mode = True

class TodoUpdateDone(BaseModel):
    done: bool

class InviteRequest(BaseModel):
    email: str
    todo_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_demo_todos(user_id: int, db: Session):
    demo_todos = [
        {
            "description": "Invite you friends!",
            "tags": ["Invite", "Friends", "Fun", "Edit"],
            "done": False,
        },
        {
            "description": "Create Your First Todo!",
            "tags": ["Create", "Register", "New", "Edit"],
            "done": True,
        }
    ]
    
    # Create and add each demo todo for the user
    for todo_data in demo_todos:
        demo_todo = Todo(
            user_id=user_id,
            description=todo_data["description"],
            tags=todo_data["tags"],
            done=todo_data["done"]
        )
        db.add(demo_todo)
    db.commit()


# Register
@app.post("/register", response_model=UserResponse)
async def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(name=user.name, email=user.email, password=user.password, invited_todo_ids=user.invited_todo_ids)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    add_demo_todos(new_user.id, db)

    return new_user

# Login 
@app.post("/login", response_model=UserResponse)
async def get_user(user_login: UserLogin, db: Annotated[Session, Depends(get_db)]):
    db_user = db.query(User).filter(User.email == user_login.email).first()
    if db_user is None or not (user_login.password == db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return db_user


# get all todos 
@app.get("/todos/{user_id}", response_model=List[TodoResponse])
def get_todos_by_user_id(user_id: int, db: Session = Depends(get_db)):
    todos = db.query(Todo).filter(Todo.user_id == user_id).all()
    
    if not todos:
        raise HTTPException(status_code=404, detail="No todos found for this user")
    
    return todos


# add new todo 
@app.post("/todos/add/{user_id}", response_model=TodoResponse)
def add_todo_for_user(user_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_todo = Todo(
        user_id=user_id,
        description=todo.description,
        tags=todo.tags,
        done=todo.done
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo

# Invite new user to your todo 
@app.post("/todo/invite", response_model=UserResponse)
def invite_user_to_todo(invite: InviteRequest, db: Session = Depends(get_db)):
    email = invite.email
    todo_id = invite.todo_id
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if todo_id not in user.invited_todo_ids:
        user.invited_todo_ids.append(todo_id)
        flag_modified(user, "invited_todo_ids")
        db.commit()
        db.refresh(user)
    
    return user

# list all invited users todo 
@app.get("/users/{user_id}/invited_todos_grouped", response_model=Dict[int, List[TodoResponse]])
def get_invited_todos_grouped_by_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    invited_todos = db.query(Todo).filter(Todo.user_id.in_(user.invited_todo_ids)).all()

    todos_by_user = defaultdict(list)
    for todo in invited_todos:
        todos_by_user[todo.user_id].append(todo)

    return dict(todos_by_user)

# update done status of todo 
@app.put("/todos/{todo_id}/done", response_model=dict)
def update_todo_done(todo_id: int, db: Session = Depends(get_db)):
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo item not found")

    todo_item.done = not todo_item.done
    db.commit()
    db.refresh(todo_item)

    return {"message": "Todo status updated successfully", "todo_id": todo_item.id, "done": todo_item.done}

# delete a todo 
@app.delete("/todos/{todo_id}", response_model=Dict[str, str])
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}
