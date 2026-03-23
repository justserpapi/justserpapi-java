import pathlib
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.normalize_openapi import normalize_spec  # noqa: E402


class NormalizeOpenApiTest(unittest.TestCase):
    def test_normalize_spec_promotes_success_response_and_auth(self):
        raw_spec = {
            "openapi": "3.1.0",
            "servers": [{"url": "http://example.com"}],
            "paths": {
                "/api/v1/google/search": {
                    "get": {
                        "tags": ["Google API"],
                        "operationId": "search",
                        "responses": {
                            "default": {
                                "description": "default response",
                                "content": {
                                    "application/json": {
                                        "examples": {
                                            "success": {
                                                "value": {
                                                    "code": 200,
                                                    "message": "success",
                                                    "data": {"items": []},
                                                    "requestId": "req_123",
                                                    "timestamp": 123456789
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {}
        }

        normalized = normalize_spec(raw_spec)

        self.assertEqual("3.0.3", normalized["openapi"])
        self.assertEqual("https://api.justserpapi.com", normalized["servers"][0]["url"])
        self.assertIn("JustSerpApiResponse", normalized["components"]["schemas"])
        self.assertIn("JustSerpApiKeyHeader", normalized["components"]["securitySchemes"])
        self.assertIn("JustSerpApiKeyQuery", normalized["components"]["securitySchemes"])

        operation = normalized["paths"]["/api/v1/google/search"]["get"]
        self.assertEqual(["Google"], operation["tags"])
        self.assertEqual(
            "#/components/schemas/JustSerpApiResponse",
            operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
        )
        self.assertEqual("Unexpected response.", operation["responses"]["default"]["description"])
        self.assertEqual(
            [{"JustSerpApiKeyHeader": [], "JustSerpApiKeyQuery": []}],
            operation["security"]
        )


if __name__ == "__main__":
    unittest.main()
