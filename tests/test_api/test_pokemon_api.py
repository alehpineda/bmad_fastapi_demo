import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.pokemon_repository import PokemonRepository, pokemon_repository

# Create a TestClient instance
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Fixture to reset the database before each test.
    This ensures test isolation.
    """
    # Reset the in-memory database by creating a new instance
    pokemon_repository.__init__()
    yield
    # Teardown is not strictly necessary here as a new instance is created
    # for the next test, but it's good practice.
    pokemon_repository.__init__()


def test_create_pokemon_success():
    """
    Test successful creation of a Pokémon.
    """
    response = client.post("/pokemon/", json={"name": "Pikachu", "type": "Electric"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Pikachu"
    assert data["type"] == "Electric"
    assert "id" in data
    assert data["id"] == 1

def test_get_all_pokemon():
    """
    Test retrieving all Pokémon.
    """
    # First, create a Pokémon
    client.post("/pokemon/", json={"name": "Charmander", "type": "Fire"})
    
    # Now, get all Pokémon
    response = client.get("/pokemon/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Charmander"

def test_create_pokemon_duplicate_name():
    """
    Test creating a Pokémon with a name that already exists (case-insensitive).
    """
    # Create the first Pokémon
    client.post("/pokemon/", json={"name": "Squirtle", "type": "Water"})
    
    # Attempt to create another with the same name but different case
    response = client.post("/pokemon/", json={"name": "squirtle", "type": "Water"})
    
    assert response.status_code == 409
    data = response.json()
    assert "already exists" in data["message"]

@pytest.mark.parametrize("payload, expected_status_code", [
    ({"type": "Grass"}, 422),  # Missing name
    ({"name": "Bulbasaur"}, 422), # Missing type
    ({"name": 123, "type": "Poison"}, 422), # Invalid name type
])
def test_create_pokemon_invalid_payload(payload, expected_status_code):
    """
    Test creating a Pokémon with various invalid payloads.
    FastAPI and Pydantic should handle this validation automatically.
    """
    response = client.post("/pokemon/", json=payload)
    assert response.status_code == expected_status_code
