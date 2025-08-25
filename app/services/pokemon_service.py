from typing import List
from app.models.pokemon_model import Pokemon, PokemonCreate
from app.repositories.pokemon_repository import PokemonRepository, pokemon_repository
from app.repositories.custom_exceptions import DuplicatePokemonError

class PokemonService:
    """
    Contains the business logic for handling Pokémon.
    """
    def __init__(self, repository: PokemonRepository):
        self._repository = repository

    def create_pokemon(self, pokemon_data: PokemonCreate) -> Pokemon:
        """
        Creates a new Pokémon after validating business rules.
        """
        # Business Rule: Check for duplicate names (case-insensitive)
        existing_pokemon = self._repository.get_by_name(pokemon_data.name)
        if existing_pokemon:
            raise DuplicatePokemonError(name=pokemon_data.name)
        
        # If validation passes, create the Pokémon
        return self._repository.create(pokemon_data)

    def get_all_pokemon(self) -> List[Pokemon]:
        """
        Retrieves all Pokémon.
        """
        return self._repository.get_all()

# Create a single instance of the service to be used as a dependency
pokemon_service = PokemonService(repository=pokemon_repository)
