from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.pokemon_model import Pokemon, PokemonCreate
from app.services.pokemon_service import PokemonService, pokemon_service
from app.repositories.custom_exceptions import DuplicatePokemonError

router = APIRouter(
    prefix="/pokemon",
    tags=["Pokemon"],
)

# Using a dependency function to make it easier to override for testing
def get_pokemon_service() -> PokemonService:
    return pokemon_service

@router.post("/", response_model=Pokemon, status_code=201)
def create_pokemon(
    pokemon_data: PokemonCreate,
    service: PokemonService = Depends(get_pokemon_service)
):
    """
    Create a new Pokémon.

    - **name**: The name of the Pokémon (must be unique).
    - **type**: The type of the Pokémon (e.g., Fire, Water).
    """
    return service.create_pokemon(pokemon_data)


@router.get("/", response_model=List[Pokemon])
def get_all_pokemon(
    service: PokemonService = Depends(get_pokemon_service)
):
    """
    Retrieve a list of all Pokémon in the system.
    """
    return service.get_all_pokemon()
