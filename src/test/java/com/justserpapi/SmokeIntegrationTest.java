package com.justserpapi;

import com.justserpapi.generated.invoker.ApiException;
import com.justserpapi.model.JustSerpApiResponse;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.EnabledIfEnvironmentVariable;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class SmokeIntegrationTest {

    @Test
    @EnabledIfEnvironmentVariable(named = "JUSTSERPAPI_API_KEY", matches = ".+")
    void autocompleteReturnsStructuredPayload() throws ApiException {
        JustSerpApiClient client = JustSerpApiClient.builder()
            .apiKey(System.getenv("JUSTSERPAPI_API_KEY"))
            .timeout(Duration.ofSeconds(30))
            .build();

        JustSerpApiResponse response = client.google().autocomplete("coffee", null, null);

        assertEquals(200, response.getCode());
        assertNotNull(response.getData());
        assertFalse(response.getData().isEmpty());
    }
}
