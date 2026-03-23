#!/usr/bin/env python3
import argparse
import copy
import json
import pathlib


SUCCESS_RESPONSE_DESCRIPTION = "Successful JustSerpAPI response."
UNEXPECTED_RESPONSE_DESCRIPTION = "Unexpected response."


def build_success_schema():
    return {
        "type": "object",
        "description": "Standard JustSerpAPI response envelope.",
        "required": ["code", "message", "data", "requestId", "timestamp"],
        "properties": {
            "code": {
                "type": "integer",
                "format": "int32",
                "description": "Application-level status code."
            },
            "message": {
                "type": "string",
                "description": "Response message."
            },
            "data": {
                "type": "object",
                "description": "Endpoint-specific payload.",
                "additionalProperties": True
            },
            "requestId": {
                "type": "string",
                "description": "Server-generated request identifier."
            },
            "timestamp": {
                "type": "integer",
                "format": "int64",
                "description": "Server timestamp in epoch milliseconds."
            }
        }
    }


def build_security_schemes():
    return {
        "JustSerpApiKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "Primary authentication header for JustSerpAPI."
        },
        "JustSerpApiKeyQuery": {
            "type": "apiKey",
            "in": "query",
            "name": "api_key",
            "description": "Compatibility fallback query parameter for JustSerpAPI."
        }
    }


def normalize_operation(operation):
    normalized = copy.deepcopy(operation)
    normalized["tags"] = ["Google"]
    responses = normalized.setdefault("responses", {})
    default_response = responses.get("default", {})
    examples = (
        default_response.get("content", {})
        .get("application/json", {})
        .get("examples", {})
    )

    success_response = {
        "description": SUCCESS_RESPONSE_DESCRIPTION,
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/JustSerpApiResponse"}
            }
        }
    }
    if examples:
        success_response["content"]["application/json"]["examples"] = copy.deepcopy(examples)
    responses["200"] = success_response
    responses["default"] = {"description": UNEXPECTED_RESPONSE_DESCRIPTION}
    normalized["security"] = [{"JustSerpApiKeyHeader": [], "JustSerpApiKeyQuery": []}]
    return normalized


def normalize_spec(document):
    normalized = copy.deepcopy(document)
    normalized["openapi"] = "3.0.3"
    normalized["servers"] = [{
        "url": "https://api.justserpapi.com",
        "description": "JustSerpAPI production server"
    }]
    normalized["tags"] = [{
        "name": "Google",
        "description": "Google search and discovery endpoints."
    }]
    normalized["security"] = [{"JustSerpApiKeyHeader": [], "JustSerpApiKeyQuery": []}]

    components = normalized.setdefault("components", {})
    schemas = components.setdefault("schemas", {})
    schemas["JustSerpApiResponse"] = build_success_schema()

    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes.update(build_security_schemes())

    paths = normalized.get("paths", {})
    for methods in paths.values():
        for method_name, operation in list(methods.items()):
            if isinstance(operation, dict):
                methods[method_name] = normalize_operation(operation)

    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize the upstream OpenAPI document for Java SDK generation.")
    parser.add_argument("--input", required=True, help="Path to the raw OpenAPI JSON.")
    parser.add_argument("--output", required=True, help="Path to write the normalized OpenAPI JSON.")
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)
    output_path = pathlib.Path(args.output)

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    normalized = normalize_spec(payload)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
