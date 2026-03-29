#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import urllib.request


DEFAULT_URL_BASE = "https://api.justserpapi.com/v3/api-docs/gateway"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch the upstream JustSerpAPI OpenAPI document.")
    parser.add_argument("--url", help="OpenAPI document URL (overrides default).")
    parser.add_argument("--api-key", help="API key to use for fetching. If not provided, reads from JUSTSERPAPI_API_KEY env var.")
    parser.add_argument("--output", required=True, help="Path to write the raw OpenAPI JSON.")
    args = parser.parse_args()

    api_url = args.url
    if not api_url:
        api_key = args.api_key or os.environ.get("JUSTSERPAPI_API_KEY")
        if not api_key:
            print("Error: API key must be provided via --api-key or JUSTSERPAPI_API_KEY environment variable.")
            return 1
        api_url = f"{DEFAULT_URL_BASE}?api_key={api_key}"

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    request = urllib.request.Request(
        api_url,
        headers={
            "Accept": "application/json",
            "User-Agent": "justserpapi-java-sdk-generator/0.1"
        }
    )

    with urllib.request.urlopen(request) as response:
        payload = json.loads(response.read().decode("utf-8"))

    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
