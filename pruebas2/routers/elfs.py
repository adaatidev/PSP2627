from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class Elf(BaseModel):
    id: int
    name: str
    turn: str
    manufactured_toys: int = Field(ge=0)


elfs_list = [
    Elf(id=1, name="Name1", turn="morning", manufactured_toys=10),
    Elf(id=2, name="Name2", turn="afternoon", manufactured_toys=65),
    Elf(id=3, name="Name3", turn="night", manufactured_toys=40),
]


def search_elf(id: int):
    for elf in elfs_list:
        if elf.id == id:
            return elf

    raise HTTPException(status_code=404, detail="Elf not found")


@router.get("")
def get_elfs():
    return elfs_list


@router.get("/notable")
def notable_elfs(min: int):
    return [elf for elf in elfs_list if elf.manufactured_toys > min]


@router.get("/{id}")
def get_elf_by_id(id: int):
    return search_elf(id)
