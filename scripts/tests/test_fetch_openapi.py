import io
import json
import os
import pathlib
import sys
import tempfile
import unittest
import urllib.error
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
    def test_build_request_uses_basic_auth_header(self):
        request = fetch_openapi.build_request(
            fetch_openapi.DEFAULT_URL_BASE,
            username="swagger-user",
            password="swagger-pass",
        )

        self.assertEqual(fetch_openapi.DEFAULT_URL_BASE, request.full_url)
        headers = {key.lower(): value for key, value in request.header_items()}
        self.assertEqual("Basic c3dhZ2dlci11c2VyOnN3YWdnZXItcGFzcw==", headers["authorization"])
        self.assertNotIn("x-api-key", headers)

    def test_build_request_supports_legacy_x_api_key_header(self):
        request = fetch_openapi.build_request(fetch_openapi.DEFAULT_URL_BASE, api_key="test-key")

        self.assertEqual(fetch_openapi.DEFAULT_URL_BASE, request.full_url)
        headers = {key.lower(): value for key, value in request.header_items()}
        self.assertEqual("test-key", headers["x-api-key"])
        self.assertNotIn("authorization", headers)

    def test_main_fetches_default_url_with_basic_auth(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = pathlib.Path(temp_dir) / "raw.json"
            with mock.patch.dict(
                os.environ,
                {
                    "JUSTSERPAPI_OPENAPI_USERNAME": "env-user",
                    "JUSTSERPAPI_OPENAPI_PASSWORD": "env-pass",
                },
                clear=False,
            ):
                with mock.patch(
                    "scripts.fetch_openapi.urllib.request.urlopen",
                    return_value=_FakeResponse({"openapi": "3.1.0"})
                ) as urlopen:
                    exit_code = fetch_openapi.main(["--output", str(output_path)])
            self.assertEqual(0, exit_code)
            request = urlopen.call_args.args[0]
            headers = {key.lower(): value for key, value in request.header_items()}
            self.assertEqual(fetch_openapi.DEFAULT_URL_BASE, request.full_url)
            self.assertEqual("Basic ZW52LXVzZXI6ZW52LXBhc3M=", headers["authorization"])
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
        self.assertNotIn("authorization", headers)

    def test_main_requires_complete_basic_auth_pair(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = pathlib.Path(temp_dir) / "raw.json"
            with mock.patch.dict(os.environ, {"JUSTSERPAPI_OPENAPI_USERNAME": "env-user"}, clear=False):
                with mock.patch("sys.stderr", new_callable=io.StringIO):
                    exit_code = fetch_openapi.main(["--output", str(output_path)])

        self.assertEqual(1, exit_code)

    def test_main_reports_basic_auth_requirement_on_401(self):
        headers = {"WWW-Authenticate": 'Basic realm="Realm"'}
        error = urllib.error.HTTPError(
            fetch_openapi.DEFAULT_URL_BASE,
            401,
            "Unauthorized",
            headers,
            io.BytesIO(b'{"code":401,"message":"Authentication failed"}'),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = pathlib.Path(temp_dir) / "raw.json"
            with mock.patch(
                "scripts.fetch_openapi.urllib.request.urlopen",
                side_effect=error,
            ):
                with mock.patch("sys.stderr", new_callable=io.StringIO):
                    exit_code = fetch_openapi.main(
                        [
                            "--username",
                            "swagger-user",
                            "--password",
                            "swagger-pass",
                            "--output",
                            str(output_path),
                        ]
                    )

        self.assertEqual(1, exit_code)


if __name__ == "__main__":
    unittest.main()
