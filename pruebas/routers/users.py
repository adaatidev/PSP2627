from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    surname: str
    age: int = Field(ge=0, le=120)


class User(UserCreate):
    id: int


class UserPatch(BaseModel):
    name: str | None = None
    surname: str | None = None
    age: int | None = Field(default=None, ge=0, le=0)


users_list = [
    User(id=0, name="Ada", surname="Atienza Devós", age=19),
    User(id=1, name="José María", surname="Gómez Vélez", age=19),
    User(id=2, name="Jorge", surname="Saldaña Carretero", age=19),
]


def search_user(id: int):
    for user in users_list:
        if user.id == id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


@router.get("")
def get_users():
    return users_list


@router.get("/")
def get_users_query(id: int):
    return search_user(id)


@router.get("/search")
def search(name: str, age: int):
    return {"searched_name": name, "searched_age": age}


@router.get("/older")
def older_users(age: int):
    return [user for user in users_list if user.age > age]


@router.get("/{id}")
def get_user_by_id(id: int):
    return search_user(id)


@router.post("", status_code=201, response_model=User)
def create_user(user: UserCreate):
    next_id = max((user.id for user in users_list), default=0) + 1
    new_user = User(id=next_id, name=user.name, surname=user.surname, age=user.age)
    users_list.append(new_user)
    return new_user


@router.put("/{id}", response_model=User)
def modify_user(id: int, data: UserCreate):
    for position, user in enumerate(users_list):
        if user.id == id:
            modified_user = User(
                id=id, name=data.name, surname=data.surname, age=data.age
            )
            users_list[position] = modified_user
            return modified_user

        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/{id}", response_model=User)
def patch_user(id: int, data: UserPatch):
    for position, user in enumerate(users_list):
        if user.id == id:
            changes = data.model_dump(exclude_uset=True, exclude_none=True)
            updated_data = user.model_dump()
            updated_data.update(changes)
            modified_user = User(**updated_data)
            users_list[position] = modified_user
            return modified_user

        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{id}")
def delete_user(id: int):
    for user in users_list:
        if user.id == id:
            users_list.remove(user)
            return {}

        raise HTTPException(status_code=404, detail="User not found")
