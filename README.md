# Read For Me

Save time reading long form essay/article/blog-post.

## Feature

- Given a URL, extracts assertions and insights into quick digestable form.
- Uses Google Gemini (get [API key](https://aistudio.google.com/app/apikey)) to summarize.

## Why

> Most books should be blog posts; most blog posts should be tweets.

Sometimes (just sometimes) the essay you're reading is better off being distilled into core arguments and assertions than being wrapped around either attractive languages or badly written prose.

This is a tool to extract these points so you can decide whether to dive into the original material or not.

Most LLMs can now do this competently enough. This tool uses Google Gemini 1.5 Flash to do it, but ideologically it's agnostic about which LLM to use.

The system prompt being used here is inspired by a pattern from [Fabric](https://github.com/danielmiessler/fabric/blob/main/patterns/summarize/dmiessler/summarize/system.md), which is responsible for producing the structure of the outcome.

## Setup

1. Create a new file `.env`, add `GEMINI_API_KEY=<your-api-key>`

## Development

1. `docker compose --profile dev run -P --rm web bash`
2. `python app.py`

## Production

1. Deploy server: `docker compose --profile prod up -d`
2. Open in browser: `http://<server>:4063`, or
3. GET `http://<server>:4063/summarize?url=<url>`
