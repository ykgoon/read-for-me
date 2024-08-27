# Read For Me

Save time reading long form articles.

## Installation

```bash
docker compose up --build
```

## Development

To enter the shell of the running `web` service for development purposes, use:

```bash
docker compose run -it --rm -P web bash
python app.py
```

### Running tests

```bash
python -m unittest tests.py
```

## Deploy

1. `docker compose up`
2. Open your browser and navigate to `http://localhost:5000`.
3. Enter a URL in the input box and click "Summarize".
