package com.justserpapi;

import com.justserpapi.generated.api.GoogleApi;
import com.justserpapi.generated.invoker.ApiClient;
import com.justserpapi.generated.invoker.auth.ApiKeyAuth;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Field;
import java.time.Duration;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

class JustSerpApiClientTest {

    @Test
    void builderAppliesBaseUrlAuthTimeoutsAndUserAgent() throws Exception {
        JustSerpApiClient client = JustSerpApiClient.builder()
            .apiKey("test-key")
            .baseUrl("https://example.com/custom/")
            .timeout(Duration.ofSeconds(5))
            .userAgent("justserpapi-java-tests")
            .build();

        ApiClient generatedApiClient = client.generatedApiClient();
        GoogleApi googleApi = client.google();

        assertEquals("https://example.com/custom", generatedApiClient.getBasePath());
        assertEquals(5000, generatedApiClient.getConnectTimeout());
        assertEquals(5000, generatedApiClient.getReadTimeout());
        assertEquals(5000, generatedApiClient.getWriteTimeout());

        ApiKeyAuth headerAuth = (ApiKeyAuth) generatedApiClient.getAuthentication("JustSerpApiKeyHeader");
        ApiKeyAuth queryAuth = (ApiKeyAuth) generatedApiClient.getAuthentication("JustSerpApiKeyQuery");
        assertEquals("test-key", headerAuth.getApiKey());
        assertEquals("test-key", queryAuth.getApiKey());

        Field defaultHeaderMapField = ApiClient.class.getDeclaredField("defaultHeaderMap");
        defaultHeaderMapField.setAccessible(true);
        @SuppressWarnings("unchecked")
        Map<String, String> defaultHeaders = (Map<String, String>) defaultHeaderMapField.get(generatedApiClient);
        assertEquals("justserpapi-java-tests", defaultHeaders.get("User-Agent"));

        assertNotNull(googleApi);
    }

    @Test
    void builderRejectsBlankApiKey() {
        assertThrows(IllegalStateException.class, () -> JustSerpApiClient.builder()
            .apiKey(" ")
            .build());
    }

    @Test
    void builderRejectsInvalidTimeout() {
        assertThrows(IllegalArgumentException.class, () -> JustSerpApiClient.builder()
            .apiKey("test-key")
            .timeout(Duration.ZERO)
            .build());
    }
}
