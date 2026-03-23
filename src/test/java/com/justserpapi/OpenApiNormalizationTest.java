package com.justserpapi;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class OpenApiNormalizationTest {
    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    @Test
    void normalizedSpecContainsStableSdkRequirements() throws Exception {
        JsonNode spec = OBJECT_MAPPER.readTree(Path.of("openapi/normalized/justserpapi-openapi.json").toFile());

        assertEquals("3.0.3", spec.path("openapi").asText());
        assertEquals("https://api.justserpapi.com", spec.path("servers").get(0).path("url").asText());

        JsonNode securitySchemes = spec.path("components").path("securitySchemes");
        assertTrue(securitySchemes.has("JustSerpApiKeyHeader"));
        assertTrue(securitySchemes.has("JustSerpApiKeyQuery"));

        JsonNode searchOperation = spec.path("paths").path("/api/v1/google/search").path("get");
        assertEquals("Google", searchOperation.path("tags").get(0).asText());
        assertEquals(
            "#/components/schemas/JustSerpApiResponse",
            searchOperation.path("responses")
                .path("200")
                .path("content")
                .path("application/json")
                .path("schema")
                .path("$ref")
                .asText()
        );

        JsonNode envelope = spec.path("components").path("schemas").path("JustSerpApiResponse");
        assertEquals("object", envelope.path("type").asText());
        assertEquals("object", envelope.path("properties").path("data").path("type").asText());
        assertTrue(envelope.path("properties").path("data").path("additionalProperties").asBoolean());
    }
}
