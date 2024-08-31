# Read For Me

Save time reading long form articles.

## Setup

```bash
docker compose build
```

## Development

```bash
docker compose run -it --rm -P web bash
python app.py
```

## Usage

1. Deploy server: `docker compose up -d`
2. Open in browser: `http://<server>:4063`


## TODO

- [ ] Return just the content, not json
- [ ] Progress indicator
- [ ] Handle request failure
- [ ] Handle API key deployment; add instructions
- [ ] Beautify front page
- [ ] Remote repo
- [ ] Transcribe YouTube
