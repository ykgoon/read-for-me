# Read For Me

Save time reading long form articles.

## Setup

1. `docker compose build`
2. Create a new file `.env`, add this

```
GEMINI_API_KEY=<your-api-key>
```

## Development

`docker compose up`

## Usage

1. Deploy server: `docker compose up -d`
2. Open in browser: `http://<server>:4063`


## TODO

- [ ] False debug flag for production mode
- [ ] Manage secret
- [ ] Transcribe YouTube
