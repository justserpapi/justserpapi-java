import json
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts import fetch_openapi  # noqa: E402


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


class FetchOpenApiTest(unittest.TestCase):
    def test_build_request_uses_x_api_key_header(self):
        request = fetch_openapi.build_request(fetch_openapi.DEFAULT_URL_BASE, "test-key")

        self.assertEqual(fetch_openapi.DEFAULT_URL_BASE, request.full_url)
        headers = {key.lower(): value for key, value in request.header_items()}
        self.assertEqual("test-key", headers["x-api-key"])
        self.assertNotIn("api_key=", request.full_url)

    def test_main_fetches_default_url_with_header_auth(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = pathlib.Path(temp_dir) / "raw.json"
            with mock.patch.dict(os.environ, {"JUSTSERPAPI_API_KEY": "env-key"}, clear=False):
                with mock.patch(
                    "scripts.fetch_openapi.urllib.request.urlopen",
                    return_value=_FakeResponse({"openapi": "3.1.0"})
                ) as urlopen:
                    exit_code = fetch_openapi.main(["--output", str(output_path)])
            self.assertEqual(0, exit_code)
            request = urlopen.call_args.args[0]
            headers = {key.lower(): value for key, value in request.header_items()}
            self.assertEqual(fetch_openapi.DEFAULT_URL_BASE, request.full_url)
            self.assertEqual("env-key", headers["x-api-key"])
            self.assertEqual("3.1.0", json.loads(output_path.read_text(encoding="utf-8"))["openapi"])

    def test_main_allows_custom_url_without_api_key(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = pathlib.Path(temp_dir) / "raw.json"
            with mock.patch(
                "scripts.fetch_openapi.urllib.request.urlopen",
                return_value=_FakeResponse({"openapi": "3.1.0"})
            ) as urlopen:
                exit_code = fetch_openapi.main(["--url", "https://example.com/openapi.json", "--output", str(output_path)])

        self.assertEqual(0, exit_code)
        request = urlopen.call_args.args[0]
        headers = {key.lower(): value for key, value in request.header_items()}
        self.assertEqual("https://example.com/openapi.json", request.full_url)
        self.assertNotIn("x-api-key", headers)


if __name__ == "__main__":
    unittest.main()
