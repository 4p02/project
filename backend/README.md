# backend

## Setting up your python environment
To setup development environment, follow these steps:

1. Setup the virtual environment:
```bash
cd backend
virtualenv .venv
source .venv/bin/activate
```

2. Install project dependencies:
```bash
pip install -e .
```

3. Run the main server entrypoint
```bash
uvicorn src.main:app --reload
```


<!-- todo: setup local database?? -->
