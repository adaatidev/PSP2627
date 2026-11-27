from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class TeamCreate(BaseModel):
    name: str
    city: str


class Team(TeamCreate):
    id: int


#   Initial data
teams_list = [
    Team(id=1, name="Lions", city="Seville"),
    Team(id=2, name="Eagles", city="Madrid"),
    Team(id=3, name="Wolves", city="Valencia"),
]


#   Returns all teams
@router.get("")
def get_teams():
    return teams_list


#   Creates a new team with an automatically generated id and returns it
@router.post("", status_code=201, response_model=Team)
def create_team(team: TeamCreate):
    #   Calculates the next id by checking the highest id on the teams list
    next_id = max((team.id for team in teams_list), default=0) + 1

    #   Creates the new team
    new_team = Team(
        id=next_id,
        name=team.name,
        city=team.city,
    )

    #   Appends the new team to the teams list
    teams_list.append(new_team)

    #   Returns the new team
    return new_team
