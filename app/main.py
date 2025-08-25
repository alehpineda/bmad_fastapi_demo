import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.endpoints import pokemon as pokemon_api
from app.repositories.custom_exceptions import DuplicatePokemonError

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler() # Log to stdout/stderr
    ]
)

app = FastAPI(
    title="BMAD FastAPI Demo",
    description="A simple API for managing Pokémon.",
    version="0.1.0",
)

@app.exception_handler(DuplicatePokemonError)
async def duplicate_pokemon_exception_handler(request: Request, exc: DuplicatePokemonError):
    """
    Handles the custom DuplicatePokemonError, returning a 409 Conflict.
    """
    return JSONResponse(
        status_code=409,
        content={"message": f"A Pokémon with the name '{exc.name}' already exists."},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catches and logs any unhandled exception that occurs in the application.
    Returns a generic 500 Internal Server Error to the client.
    """
    # Using logger.exception() automatically includes exception info and traceback
    logging.getLogger(__name__).exception("An unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred on the server."},
    )

@app.get("/", tags=["Root"])
async def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Pokémon API!"}

@app.get("/error", tags=["Test"])
async def trigger_error():
    """A temporary endpoint to test the exception handler and logging."""
    raise ValueError("This is a test exception to verify logging.")

# Include the API router
app.include_router(pokemon_api.router)
