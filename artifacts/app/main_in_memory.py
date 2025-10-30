from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    role: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    role: str

fake_users_db = []
user_id_counter = 1

app = FastAPI()

@app.post("/users/", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate):
    global user_id_counter
    user_dict = user.dict()
    user_dict["id"] = user_id_counter
    fake_users_db.append(user_dict)
    user_id_counter += 1
    return user_dict

@app.get("/users/", response_model=list[UserRead])
async def read_users():
    return fake_users_db

@app.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int):
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")