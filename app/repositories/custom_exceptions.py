class DuplicatePokemonError(Exception):
    """Custom exception raised when attempting to add a Pokémon that already exists."""
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"A Pokémon with the name '{name}' already exists.")
