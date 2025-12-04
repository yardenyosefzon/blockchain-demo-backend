# Blockchain Demo Backend

Lightweight Flask API that exposes an in-memory blockchain, wallets, and transactions for learning and demos.

## Quick start
- Install deps: `pip install -r requirements.txt`
- Run: `flask run` (or `python app.py`)
- Base URL: `http://localhost:5000/v1`

## API overview (resourceful paths)
- Health: `GET /v1/health`
- Blocks: `GET /v1/blocks`, `GET /v1/blocks/<index>`, `PATCH /v1/blocks/<index>`, `POST /v1/blocks/<index>/remine`, `GET /v1/blocks/validation`
- Mining: `POST /v1/mining/blocks`, `GET /v1/mining/reward`
- Transactions: `GET /v1/transactions/mempool`, `POST /v1/transactions/draft`, `POST /v1/transactions`
- Wallets: `GET /v1/wallets`, `POST /v1/wallets`, `GET /v1/wallets/<address>`, `GET /v1/wallets/<address>/balance`, `POST /v1/wallets/pending-balances`
- Admin: `POST /v1/admin/reset`, `POST /v1/admin/mock-seed`

Responses are wrapped in `ApiResponse` with `data`, `error`, and `success` fields. This project is for demo use only; secrets (wallet private keys) are returned in wallet payloads by design.

## Project layout
- `app.py` — Flask app factory and blueprint registration
- `api/routes/` — route groups (blocks, mining, transactions, wallets, admin, health)
- `api/core/` — blockchain and wallet core logic
- `api/schemas/` — Marshmallow schemas for request validation
- `api/utils/` — response/validation helpers
- `api/state.py` — in-memory blockchain and wallet registry

## Development tips
- Keep `api/state.py` in-memory state isolated per process; restart the server for a clean slate or call `POST /v1/admin/reset`.
- Add new endpoints via a sub-blueprint under `api/routes/` and register it in `api/routes/__init__.py`.
- Use the Marshmallow schemas in `api/schemas` with `@validate_json` to enforce request shapes.
