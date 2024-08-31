# Read For Me

Save time reading long form articles.

## Setup

```bash
docker compose build
```

## Development

```bash
docker compose run -e GEMINI_API_KEY="api-key" -it --rm -P web python app.py
```

## Usage

1. Deploy server: `docker compose up -d`
2. Open in browser: `http://<server>:4063`


## TODO

- [ ] Remote repo
- [ ] Handle API key deployment; add instructions
- [ ] False debug flag for production mode
- [ ] Manage secret
- [ ] Transcribe YouTube
