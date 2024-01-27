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
uvicorn backend.main:app --reload
```

## TODO

Look for TODO comments, although
- Setup database!!!
- Decide if we are going to use posgrest or use graphql
- Implement register method in database
- Implement login method in database
- Implement oauth 
- Implement summerize
- Implement shorten (like this right? example: https://www.google.com/ -> https://www.ourdomain.com/RDsfOs)