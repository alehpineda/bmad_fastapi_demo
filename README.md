# bmad_fastapi_demo

This is a test project using bmad method to create a fastapi get and post endpoints. It's pokemon themed. It should use uv for environment and dependency managment, python 3.13, latest fastapi. Must have unit testing.

## Getting Started

### Prerequisites

- Python 3.13+
- `uv` package manager (`pip install uv`)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd bmad_fastapi_demo
    ```

2.  **Create and activate the virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

### Running the Application

To run the development server, use the following command:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
