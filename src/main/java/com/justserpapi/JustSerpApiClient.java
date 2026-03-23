package com.justserpapi;

import com.justserpapi.generated.api.GoogleApi;
import com.justserpapi.generated.invoker.ApiClient;
import com.justserpapi.generated.invoker.auth.ApiKeyAuth;
import com.justserpapi.generated.invoker.auth.Authentication;

import java.net.URI;
import java.time.Duration;
import java.util.Objects;

/**
 * Stable SDK entry point for configuring and accessing generated JustSerpAPI operations.
 */
public final class JustSerpApiClient {
    static final String DEFAULT_BASE_URL = "https://api.justserpapi.com";
    static final String DEFAULT_USER_AGENT = "justserpapi-java";
    static final Duration DEFAULT_TIMEOUT = Duration.ofSeconds(30);

    private final ApiClient apiClient;
    private final GoogleApi googleApi;

    private JustSerpApiClient(Builder builder) {
        this.apiClient = new ApiClient();
        this.apiClient.setBasePath(normalizeBaseUrl(builder.baseUrl));
        this.apiClient.setUserAgent(builder.userAgent);
        this.apiClient.setConnectTimeout(toMillis(builder.connectTimeout, "connectTimeout"));
        this.apiClient.setReadTimeout(toMillis(builder.readTimeout, "readTimeout"));
        this.apiClient.setWriteTimeout(toMillis(builder.writeTimeout, "writeTimeout"));
        this.apiClient.setDebugging(builder.debugging);
        setApiKey(this.apiClient, builder.apiKey);
        this.googleApi = new GoogleApi(apiClient);
    }

    public static Builder builder() {
        return new Builder();
    }

    public GoogleApi google() {
        return googleApi;
    }

    ApiClient generatedApiClient() {
        return apiClient;
    }

    private static void setApiKey(ApiClient apiClient, String apiKey) {
        updateApiKey(apiClient.getAuthentication("JustSerpApiKeyHeader"), apiKey);
        updateApiKey(apiClient.getAuthentication("JustSerpApiKeyQuery"), apiKey);
    }

    private static void updateApiKey(Authentication authentication, String apiKey) {
        if (authentication instanceof ApiKeyAuth) {
            ((ApiKeyAuth) authentication).setApiKey(apiKey);
            return;
        }
        throw new IllegalStateException("Expected ApiKeyAuth but got " + authentication);
    }

    private static String normalizeBaseUrl(String baseUrl) {
        URI uri = URI.create(Objects.requireNonNull(baseUrl, "baseUrl must not be null"));
        if (uri.getScheme() == null || uri.getHost() == null) {
            throw new IllegalArgumentException("baseUrl must be an absolute HTTP(S) URL");
        }
        String normalized = uri.toString();
        while (normalized.endsWith("/")) {
            normalized = normalized.substring(0, normalized.length() - 1);
        }
        return normalized;
    }

    private static int toMillis(Duration timeout, String fieldName) {
        Objects.requireNonNull(timeout, fieldName + " must not be null");
        if (timeout.isZero() || timeout.isNegative()) {
            throw new IllegalArgumentException(fieldName + " must be greater than zero");
        }
        long millis = timeout.toMillis();
        if (millis > Integer.MAX_VALUE) {
            throw new IllegalArgumentException(fieldName + " exceeds Integer.MAX_VALUE milliseconds");
        }
        return (int) millis;
    }

    public static final class Builder {
        private String apiKey;
        private String baseUrl = DEFAULT_BASE_URL;
        private String userAgent = DEFAULT_USER_AGENT;
        private boolean debugging;
        private Duration connectTimeout = DEFAULT_TIMEOUT;
        private Duration readTimeout = DEFAULT_TIMEOUT;
        private Duration writeTimeout = DEFAULT_TIMEOUT;

        private Builder() {
        }

        public Builder apiKey(String apiKey) {
            this.apiKey = apiKey;
            return this;
        }

        public Builder baseUrl(String baseUrl) {
            this.baseUrl = baseUrl;
            return this;
        }

        public Builder timeout(Duration timeout) {
            this.connectTimeout = timeout;
            this.readTimeout = timeout;
            this.writeTimeout = timeout;
            return this;
        }

        public Builder connectTimeout(Duration connectTimeout) {
            this.connectTimeout = connectTimeout;
            return this;
        }

        public Builder readTimeout(Duration readTimeout) {
            this.readTimeout = readTimeout;
            return this;
        }

        public Builder writeTimeout(Duration writeTimeout) {
            this.writeTimeout = writeTimeout;
            return this;
        }

        public Builder userAgent(String userAgent) {
            this.userAgent = userAgent;
            return this;
        }

        public Builder debugging(boolean debugging) {
            this.debugging = debugging;
            return this;
        }

        public JustSerpApiClient build() {
            if (apiKey == null || apiKey.isBlank()) {
                throw new IllegalStateException("apiKey must be provided");
            }
            if (userAgent == null || userAgent.isBlank()) {
                throw new IllegalStateException("userAgent must be provided");
            }
            return new JustSerpApiClient(this);
        }
    }
}
