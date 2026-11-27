from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class PlayerCreate(BaseModel):
    name: str
    age: int = Field(ge=0)
    goals: int = Field(ge=0)


class Player(PlayerCreate):
    id: int


class PlayerPatch(BaseModel):
    goals: int = Field(ge=0)


#   Initial data
players_list = [
    Player(id=1, name="Hugo", age=23, goals=12),
    Player(id=2, name="Alex", age=20, goals=4),
    Player(id=3, name="Leo", age=27, goals=15),
    Player(id=4, name="Noah", age=19, goals=1),
    Player(id=5, name="Marc", age=25, goals=8),
]


#   Function to search a player based on their id (auxiliar function)
def search_player(id: int):
    for player in players_list:
        if player.id == id:
            return player

    raise HTTPException(status_code=404, detail="Player not found")


#   Returns all players
@router.get("")
def get_players():
    return players_list


#   Returns a list of players whose number of goals is strictly greater than the average number of goals of all current players
@router.get("/above-average")
def get_above_average_players():
    #   If the players list is empty the function returns
    if len(players_list) == 0:
        return []

    #   Calculates the total goals
    total_goals = 0
    for player in players_list:
        total_goals += player.goals

    #   Calculates the average goals
    average_goals = total_goals / len(players_list)

    #   Checks the goals of the players from the list, if the players goals is above the average it appends on a new list
    above_average_list = []
    for player in players_list:
        if player.goals > average_goals:
            above_average_list.append(player)

    #   It returns the list of players who have goals above the average
    return above_average_list


#   Returns a player by id
@router.get("/{id}")
def get_player_by_id(id: int):
    return search_player(id)


#   Creates a player and returns it
@router.post("", status_code=201, response_model=Player)
def create_player(player: PlayerCreate):
    #   Calculates the next id by checking the highest id in the players list
    next_id = max((player.id for player in players_list), default=0) + 1

    #   Creates the new player
    new_player = Player(
        id=next_id,
        name=player.name,
        age=player.age,
        goals=player.goals,
    )

    #   Appends the new player to the players list
    players_list.append(new_player)

    #   Returns the new player
    return new_player


#   Updates name, age and goals but it keeps the id (update a player)
@router.put("/{id}", response_model=Player)
def modify_player(id: int, data: PlayerCreate):
    for position, player in enumerate(players_list):
        if player.id == id:
            modified_player = Player(
                id=id,
                name=data.name,
                age=data.age,
                goals=data.goals,
            )
            players_list[position] = modified_player
            return modified_player

    raise HTTPException(status_code=404, detail="Player not found")


#   Updates only the goals field, keeping the others fields
@router.patch("/{id}", response_model=Player)
def patch_player(id: int, data: PlayerPatch):
    for position, player in enumerate(players_list):
        if player.id == id:
            patched_player = Player(
                id=player.id,
                name=player.name,
                age=player.age,
                goals=data.goals,
            )
            players_list[position] = patched_player
            return patched_player

    raise HTTPException(status_code=404, detail="Player not found")


#   Deletes the player and returns a confirmation
@router.delete("/{id}")
def delete_player(id: int):
    for player in players_list:
        if player.id == id:
            players_list.remove(player)
            return {"confirmation": "Player deleted successfully"}

    raise HTTPException(status_code=404, detail="Player not found")
