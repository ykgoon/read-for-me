# Read For Me

Save time reading long form articles.

## Feature

Given a URL of a long form essay/article/blog-post, extracts assertions and insights into easily digestable form.

## Setup

1. `docker compose --profile dev build`
2. Create a new file `.env`, add this

```
GEMINI_API_KEY=<your-api-key>
```

## Development

`docker compose --profile dev up`

## Production

1. Deploy server: `docker compose --profile prod up -d`
2. Open in browser: `http://<server>:4063`
