<p align="center">
  <img src="https://justserpapi.com/logo/whiteBgColor.png" alt="JustSerpAPI Logo" width="200">
</p>

<h1 align="center">JustSerpAPI Java SDK</h1>

[![Maven Central](https://img.shields.io/maven-central/v/com.justserpapi/justserpapi-java)](https://central.sonatype.com/artifact/com.justserpapi/justserpapi-java)
[![Java](https://img.shields.io/badge/java-11%2B-2f81f7)](https://www.oracle.com/java/technologies/downloads/)
[![Docs](https://img.shields.io/badge/docs-justserpapi.com-32c955)](https://docs.justserpapi.com/?utm_source=github&utm_medium=referral&utm_campaign=justserpapi_justserpapi_java&utm_content=repo_readme)
[![License](https://img.shields.io/badge/license-Apache%202.0-f28c28)](LICENSE)

Official Java SDK for [JustSerpAPI]([https://justserpapi.com/](https://justserpapi.com/?utm_source=github&utm_medium=referral&utm_campaign=justserpapi_justserpapi_java&utm_content=repo_readme).

Use this SDK to access JustSerpAPI from Java and fetch structured Google search results without building raw HTTP requests by hand.

Get your API key, product docs, and pricing at [justserpapi.com]([https://justserpapi.com/](https://justserpapi.com/?utm_source=github&utm_medium=referral&utm_campaign=justserpapi_justserpapi_java&utm_content=repo_readme)).

## Requirements

- Java 11+

## Installation

```xml
<dependency>
  <groupId>com.justserpapi</groupId>
  <artifactId>justserpapi-java</artifactId>
  <version>0.1.0</version>
</dependency>
```

## Quick Start

```java
import com.justserpapi.JustSerpApiClient;
import com.justserpapi.generated.invoker.ApiException;
import com.justserpapi.model.JustSerpApiResponse;

import java.time.Duration;

public class Example {
    public static void main(String[] args) throws ApiException {
        JustSerpApiClient client = JustSerpApiClient.builder()
            .apiKey(System.getenv("JUSTSERPAPI_API_KEY"))
            .timeout(Duration.ofSeconds(30))
            .build();

        JustSerpApiResponse response = client.google().search(
            "coffee shops in shanghai",
            0,
            false,
            "en",
            null,
            "google.com",
            "us",
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            "off",
            "0",
            "1"
        );

        System.out.println("code = " + response.getCode());
        System.out.println("message = " + response.getMessage());
        System.out.println("requestId = " + response.getRequestId());
        System.out.println("organic results = " + response.getData().get("organic_results"));
    }
}
```

## Configuration

```java
JustSerpApiClient client = JustSerpApiClient.builder()
    .apiKey("YOUR_API_KEY")
    .baseUrl("https://api.justserpapi.com")
    .timeout(Duration.ofSeconds(30))
    .build();
```

`apiKey(...)` is required. `baseUrl(...)` and `timeout(...)` are optional.

## Response Format

Every request returns a `JustSerpApiResponse` envelope:

- `code`: application-level status code
- `message`: response message
- `requestId`: server request id
- `timestamp`: epoch milliseconds
- `data`: endpoint-specific payload

## Documentation

- Website: [https://justserpapi.com/](https://justserpapi.com/)
- API docs: [https://justserpapi.com/](https://justserpapi.com/)
- GitHub releases: [https://github.com/justserpapi/justserpapi-java/releases](https://github.com/justserpapi/justserpapi-java/releases)

## Support

For account setup, API access, and product information, start at [justserpapi.com](https://justserpapi.com/).
