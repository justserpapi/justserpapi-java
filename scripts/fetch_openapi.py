#!/usr/bin/env python3
import argparse
import base64
import json
import os
import pathlib
import sys
from typing import List, Optional
import urllib.error
import urllib.request


DEFAULT_URL_BASE = "https://api.justserpapi.com/v3/api-docs/gateway"
USER_AGENT = "justserpapi-java-sdk-generator/0.1"
OPENAPI_USERNAME_ENV = "JUSTSERPAPI_OPENAPI_USERNAME"
OPENAPI_PASSWORD_ENV = "JUSTSERPAPI_OPENAPI_PASSWORD"
API_KEY_ENV = "JUSTSERPAPI_API_KEY"


def build_request(
    api_url: str,
    api_key: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> urllib.request.Request:
    headers = {
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if username is not None and password is not None:
        token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
        headers["Authorization"] = f"Basic {token}"
    elif api_key:
        headers["X-API-Key"] = api_key
    return urllib.request.Request(api_url, headers=headers)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch the upstream JustSerpAPI OpenAPI document.")
    parser.add_argument("--url", help="OpenAPI document URL (overrides default).")
    parser.add_argument("--api-key", help=f"Legacy API key to use for fetching. If not provided, reads from {API_KEY_ENV} env var.")
    parser.add_argument("--username", help=f"HTTP Basic auth username. If not provided, reads from {OPENAPI_USERNAME_ENV} env var.")
    parser.add_argument("--password", help=f"HTTP Basic auth password. If not provided, reads from {OPENAPI_PASSWORD_ENV} env var.")
    parser.add_argument("--output", required=True, help="Path to write the raw OpenAPI JSON.")
    args = parser.parse_args(argv)

    api_key = args.api_key or os.environ.get(API_KEY_ENV)
    username = args.username or os.environ.get(OPENAPI_USERNAME_ENV)
    password = args.password or os.environ.get(OPENAPI_PASSWORD_ENV)
    api_url = args.url or DEFAULT_URL_BASE
    if (username and not password) or (password and not username):
        print(
            f"Error: both username and password must be provided via --username/--password or {OPENAPI_USERNAME_ENV}/{OPENAPI_PASSWORD_ENV}.",
            file=sys.stderr,
        )
        return 1
    if not ((username and password) or api_key) and not args.url:
        print(
            f"Error: credentials must be provided via --username/--password, {OPENAPI_USERNAME_ENV}/{OPENAPI_PASSWORD_ENV}, or legacy --api-key/{API_KEY_ENV}.",
            file=sys.stderr,
        )
        return 1

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    request = build_request(api_url, api_key=api_key, username=username, password=password)

    try:
        with urllib.request.urlopen(request) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace").strip()
        auth_scheme = exc.headers.get("WWW-Authenticate", "")
        print(f"Error: failed to fetch OpenAPI document from {api_url} (HTTP {exc.code}).", file=sys.stderr)
        if exc.code == 401:
            if auth_scheme.startswith("Basic"):
                print(
                    f"The upstream docs endpoint requires HTTP Basic auth. Check {OPENAPI_USERNAME_ENV}/{OPENAPI_PASSWORD_ENV}.",
                    file=sys.stderr,
                )
            elif username and password:
                print("The provided HTTP Basic auth credentials were rejected.", file=sys.stderr)
            elif api_key:
                print(f"The legacy API key was rejected. Check {API_KEY_ENV}.", file=sys.stderr)
        if body:
            print(body, file=sys.stderr)
        return 1

    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
