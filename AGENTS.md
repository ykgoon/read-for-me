## Development

Runtime is from within Docker container. To run a Python script, do not just run `python <script>` but do it with `docker compose --profile dev run -P --rm web python <script>`.

When Python packages are updated, the corresponding Docker image will need to be updated with `docker compose --profile dev build`.

## Running tests

There are no automated test cases here.

If you need to run tests, write partial snippets into a temporary test file, then run it with `docker compose ... python <script>` above.
