#  Generating FastAPI app with in-memory database
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Literal
from datetime import datetime
from threading import Lock

app = FastAPI()

# Pydantic models

class UserBase(BaseModel):
    company_id: int
    email: EmailStr
    password_hash: str = Field(..., min_length=1)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    role: Literal['Admin', 'Hiring Manager', 'New Hire']
    manager_id: Optional[int] = None

    @validator('first_name', 'last_name')
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError('Must not be empty')
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    company_id: Optional[int] = None
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = Field(None, min_length=1)
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    role: Optional[Literal['Admin', 'Hiring Manager', 'New Hire']] = None
    manager_id: Optional[int] = None

    @validator('first_name', 'last_name')
    def not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Must not be empty')
        return v

class UserOut(UserBase):
    user_id: int
    created_at: str
    updated_at: str

# In-memory repository

class InMemoryUserRepo:
    def __init__(self):
        self._users = {}
        self._id_counter = 2
        self._lock = Lock()
        now = datetime.utcnow().isoformat()
        # Seed user: id=1
        self._users[1] = {
            'user_id': 1,
            'company_id': 1,
            'email': 'admin@example.com',
            'password_hash': 'hashed_pw',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'Admin',
            'manager_id': None,
            'created_at': now,
            'updated_at': now
        }

    def list(self) -> List[dict]:
        return list(self._users.values())

    def get(self, user_id: int) -> Optional[dict]:
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[dict]:
        for user in self._users.values():
            if user['email'].lower() == email.lower():
                return user
        return None

    def create(self, data: UserCreate) -> dict:
        with self._lock:
            if self.find_by_email(data.email):
                raise ValueError('Email already exists')
            now = datetime.utcnow().isoformat()
            user = data.dict()
            user_id = self._id_counter
            self._id_counter += 1
            user['user_id'] = user_id
            user['created_at'] = now
            user['updated_at'] = now
            self._users[user_id] = user
            return user

    def update(self, user_id: int, data: UserUpdate) -> dict:
        with self._lock:
            user = self._users.get(user_id)
            if not user:
                raise KeyError
            update_data = data.dict(exclude_unset=True)
            if 'email' in update_data:
                existing = self.find_by_email(update_data['email'])
                if existing and existing['user_id'] != user_id:
                    raise ValueError('Email already exists')
            for k, v in update_data.items():
                user[k] = v
            user['updated_at'] = datetime.utcnow().isoformat()
            return user

    def delete(self, user_id: int):
        with self._lock:
            if user_id not in self._users:
                raise KeyError
            del self._users[user_id]

    def exists(self, user_id: int) -> bool:
        return user_id in self._users

repo = InMemoryUserRepo()

# Helper: Validate manager_id exists or is None

def validate_manager_id(manager_id: Optional[int]):
    if manager_id is not None and not repo.exists(manager_id):
        raise HTTPException(status_code=400, detail='manager_id does not exist')

# Endpoints

@app.get("/users", response_model=List[UserOut])
def list_users():
    return [UserOut(**user) for user in repo.list()]

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user)

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user_in: UserCreate):
    validate_manager_id(user_in.manager_id)
    try:
        user = repo.create(user_in)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return UserOut(**user)

@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_in: UserUpdate):
    if user_in.manager_id is not None:
        validate_manager_id(user_in.manager_id)
    try:
        user = repo.update(user_id, user_in)
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found")
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return UserOut(**user)

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    try:
        repo.delete(user_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found")
    return None
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Literal
from datetime import datetime
from threading import Lock

app = FastAPI()

# Pydantic models

class UserBase(BaseModel):
    company_id: int
    email: EmailStr
    password_hash: str = Field(..., min_length=1)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    role: Literal['Admin', 'Hiring Manager', 'New Hire']
    manager_id: Optional[int] = None

    @validator('first_name', 'last_name')
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError('Must not be empty')
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    company_id: Optional[int] = None
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = Field(None, min_length=1)
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    role: Optional[Literal['Admin', 'Hiring Manager', 'New Hire']] = None
    manager_id: Optional[int] = None

    @validator('first_name', 'last_name')
    def not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Must not be empty')
        return v

class UserOut(UserBase):
    user_id: int
    created_at: str
    updated_at: str

# In-memory repository

class InMemoryUserRepo:
    def __init__(self):
        self._users = {}
        self._id_counter = 2
        self._lock = Lock()
        now = datetime.utcnow().isoformat()
        # Seed user: id=1
        self._users[1] = {
            'user_id': 1,
            'company_id': 1,
            'email': 'admin@example.com',
            'password_hash': 'hashed_pw',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'Admin',
            'manager_id': None,
            'created_at': now,
            'updated_at': now
        }

    def list(self) -> List[dict]:
        return list(self._users.values())

    def get(self, user_id: int) -> Optional[dict]:
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[dict]:
        for user in self._users.values():
            if user['email'].lower() == email.lower():
                return user
        return None

    def create(self, data: UserCreate) -> dict:
        with self._lock:
            if self.find_by_email(data.email):
                raise ValueError('Email already exists')
            now = datetime.utcnow().isoformat()
            user = data.dict()
            user_id = self._id_counter
            self._id_counter += 1
            user['user_id'] = user_id
            user['created_at'] = now
            user['updated_at'] = now
            self._users[user_id] = user
            return user

    def update(self, user_id: int, data: UserUpdate) -> dict:
        with self._lock:
            user = self._users.get(user_id)
            if not user:
                raise KeyError
            update_data = data.dict(exclude_unset=True)
            if 'email' in update_data:
                existing = self.find_by_email(update_data['email'])
                if existing and existing['user_id'] != user_id:
                    raise ValueError('Email already exists')
            for k, v in update_data.items():
                user[k] = v
            user['updated_at'] = datetime.utcnow().isoformat()
            return user

    def delete(self, user_id: int):
        with self._lock:
            if user_id not in self._users:
                raise KeyError
            del self._users[user_id]

    def exists(self, user_id: int) -> bool:
        return user_id in self._users

repo = InMemoryUserRepo()

# Helper: Validate manager_id exists or is None

def validate_manager_id(manager_id: Optional[int]):
    if manager_id is not None and not repo.exists(manager_id):
        raise HTTPException(status_code=400, detail='manager_id does not exist')

# Endpoints

@app.get("/users", response_model=List[UserOut])
def list_users():
    return [UserOut(**user) for user in repo.list()]

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user)

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user_in: UserCreate):
    validate_manager_id(user_in.manager_id)
    try:
        user = repo.create(user_in)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return UserOut(**user)

@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_in: UserUpdate):
    if user_in.manager_id is not None:
        validate_manager_id(user_in.manager_id)
    try:
        user = repo.update(user_id, user_in)
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found")
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return UserOut(**user)

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    try:
        repo.delete(user_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found")
    return None
