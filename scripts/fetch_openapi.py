#!/usr/bin/env python3
import argparse
import json
import pathlib
import urllib.request


DEFAULT_URL = "https://api.justserpapi.com/v3/api-docs/gateway?api_key=9KsZprZU"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch the upstream JustSerpAPI OpenAPI document.")
    parser.add_argument("--url", default=DEFAULT_URL, help="OpenAPI document URL.")
    parser.add_argument("--output", required=True, help="Path to write the raw OpenAPI JSON.")
    args = parser.parse_args()

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    request = urllib.request.Request(
        args.url,
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
