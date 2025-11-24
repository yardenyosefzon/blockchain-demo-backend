#!/usr/bin/env python3
import argparse
import os
import time
from typing import Optional

import requests


def mine_forever_http(api_url: str, miner_address: str, interval: int = 5, timeout: int = 5):
    """
    Poll the API's mempool and trigger mining via HTTP so this process
    acts on the same state as the Flask server.

    - api_url: base URL of the API (e.g. http://localhost:5000)
    - miner_address: address that receives the coinbase reward
    - interval: seconds to wait between polls
    - timeout: per-request timeout in seconds
    """
    mempool_url = f"{api_url.rstrip('/')}/api/mempool"
    mine_url = f"{api_url.rstrip('/')}/api/mine"

    while True:
        try:
            r = requests.get(mempool_url, timeout=timeout)
            r.raise_for_status()
            mempool = r.json() or []
        except Exception as e:
            print(f"[miner] Error fetching mempool: {e}")
            time.sleep(interval)
            continue

        if mempool:
            try:
                resp = requests.post(mine_url, json={"miner": miner_address}, timeout=timeout)
                if resp.ok:
                    print(f"[miner] Mined block for {miner_address}. mempool_before={len(mempool)}")
                else:
                    print(f"[miner] Mine request failed: {resp.status_code} {resp.text}")
            except Exception as e:
                print(f"[miner] Error mining: {e}")
        else:
            print("[miner] Mempool empty, waiting...")

        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="Mine pending transactions forever via HTTP.")
    parser.add_argument("--miner", required=True, help="Miner address to receive rewards")
    parser.add_argument("--interval", type=int, default=5, help="Polling interval (seconds)")
    parser.add_argument(
        "--api-url",
        default=os.getenv("API_URL", "http://127.0.0.1:5000"),
        help="Base URL for the API (default: %(default)s)",
    )
    parser.add_argument("--timeout", type=int, default=5, help="HTTP request timeout (seconds)")
    args = parser.parse_args()

    print(
        f"Starting miner for {args.miner} against {args.api_url} (interval={args.interval}s, timeout={args.timeout}s)..."
    )
    try:
        mine_forever_http(args.api_url, args.miner, interval=args.interval, timeout=args.timeout)
    except KeyboardInterrupt:
        print("\nMiner stopped.")


if __name__ == "__main__":
    main()
