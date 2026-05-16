# AnswerLayer Embed API Demo

A single-page, dependency-free reference client for the AnswerLayer embed API.
It loads a dashboard manifest, fetches paginated tile data, and shows how a
host application turns the manifest's typed `visualization` encoding into a
rendered chart.

Everything is in one file (`index.html`) — inline HTML, CSS, and vanilla JS,
no build step. `serve.py` is an optional static server that disables caching
so edits show up on reload.

## Running

```bash
python3 serve.py            # http://localhost:5174
python3 serve.py 8080       # custom port
```

Plain `python3 -m http.server` works too; opening `index.html` directly as a
`file://` URL also works, subject to the API's CORS policy.

Then in the page:

1. Set **API base URL** (e.g. `http://localhost:8000`), **Dashboard ID**, and
   an **API key**.
2. **Load Manifest** — fetches the dashboard's tile list.
3. **Fetch Tile Data** — fetches each tile's data.
4. **Fetch Again** — repeats the request; the `cache_hit` badge flips to
   `true` when the backend serves from cache.
5. **Use Unique Filter** — injects a one-off filter so the next fetch misses
   the cache.

Form values persist to `localStorage`.

## API surface exercised

| Call | Purpose |
|------|---------|
| `GET /api/v1/dashboards/{id}/manifest` | Tile list with `tile_key`, the typed `visualization` encoding, `data_url`, and pagination defaults |
| `POST {tile.data_url}` | Tile data; supports `filters` and cursor pagination |
| `POST {tile.data_url}` with `result_handle` + `pagination.cursor` | Next page of a materialized result (the handle must be one this tile produced) |

Requests authenticate with an `X-API-Key` header.

### Tile data response

```jsonc
{
  "columns": ["region", "revenue"],
  "rows": [["west", 1200], ["east", 980]],
  "row_count": 2,
  "total_rows": 2,
  "next_cursor": null,        // present when more pages exist
  "result_handle": null,      // present when the result was materialized
  "cache_hit": false,
  "execution_time_ms": 41,
  "computed_at": "2026-05-16T01:00:00Z",
  "encoding_warnings": []     // non-empty if the encoding references missing columns
}
```

Small results come back inline. Larger results are materialized server-side
and returned with a `result_handle` and `next_cursor`; pass both back to page
through the data.

## Rendering

Each manifest tile carries a typed `visualization` object whose `encoding`
maps a chart role to a column name. The demo reads roles straight from it —
no column-name or key-casing guessing:

- **chart type** — `visualization.chart_type` (`metric`, `bar`, `line`, `area`, `donut`, `table`)
- **x / label field** — `encoding.x` (axis charts) or `encoding.label` (donut)
- **value fields** — `encoding.value` (metric/donut) or `encoding.y` (axis charts)

It resolves each role to a column, finds that column's index in the response
`columns`, and draws a metric, bar, or table preview. If a tile's response
carries `encoding_warnings`, the demo shows them — the saved query no longer
returns a column the encoding names. A host application is free to ignore the
preview and feed columns/rows into its own charting library.

## License

MIT — see [LICENSE](LICENSE).
