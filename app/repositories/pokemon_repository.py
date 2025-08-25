from typing import List, Optional
from app.models.pokemon_model import Pokemon, PokemonCreate
from app.repositories.custom_exceptions import DuplicatePokemonError

class PokemonRepository:
    """
    Handles the data access logic for Pokémon.
    This is an in-memory implementation.
    """
    def __init__(self):
        self._pokemon_db: List[Pokemon] = []
        self._next_id = 1

    def get_by_name(self, name: str) -> Optional[Pokemon]:
        """
        Retrieves a Pokémon by its name (case-insensitive).
        """
        for pokemon in self._pokemon_db:
            if pokemon.name.lower() == name.lower():
                return pokemon
        return None

    def create(self, pokemon_data: PokemonCreate) -> Pokemon:
        """
        Creates a new Pokémon and adds it to the database.
        """
        new_pokemon = Pokemon(
            id=self._next_id,
            name=pokemon_data.name,
            type=pokemon_data.type
        )
        self._pokemon_db.append(new_pokemon)
        self._next_id += 1
        return new_pokemon

    def get_all(self) -> List[Pokemon]:
        """
        Retrieves all Pokémon from the database.
        """
        return self._pokemon_db

# Create a single instance of the repository to be used as a dependency
pokemon_repository = PokemonRepository()
