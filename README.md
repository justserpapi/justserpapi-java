# JustSerpAPI Java SDK

Java SDK for the JustSerpAPI HTTP interface. The SDK is generated from the upstream OpenAPI document and republished through GitHub and Maven Central.

## What This Repository Contains

- Checked-in raw and normalized OpenAPI specs under `openapi/`
- Checked-in generated Java sources under `src/main/generated/`
- A stable entry point, `JustSerpApiClient`, under `src/main/java/`
- GitHub Actions for CI, scheduled spec sync PRs, and tag-based releases

## Requirements

- Java 11+
- Python 3.9+
- Maven 3.9+

## Install

```xml
<dependency>
  <groupId>com.justserpapi</groupId>
  <artifactId>justserpapi-java</artifactId>
  <version>0.1.0</version>
</dependency>
```

Replace the version with the latest published release.

## Usage

```java
import com.justserpapi.JustSerpApiClient;
import com.justserpapi.model.JustSerpApiResponse;

import java.time.Duration;

public class Example {
    public static void main(String[] args) throws Exception {
        JustSerpApiClient client = JustSerpApiClient.builder()
            .apiKey(System.getenv("JUSTSERPAPI_API_KEY"))
            .timeout(Duration.ofSeconds(30))
            .build();

        JustSerpApiResponse response = client.google().autocomplete("coffee", null, null);
        System.out.println(response.getCode());
        System.out.println(response.getData());
    }
}
```

`JustSerpApiClient` configures base URL, timeout, user agent, and API key injection. Operation methods are generated from the normalized OpenAPI document and exposed through `client.google()`.

## Regenerate The SDK

Fetch the live OpenAPI document, normalize it, regenerate the SDK, and sync checked-in generated sources:

```bash
python3 scripts/sync_sdk.py
```

Rebuild from the checked-in normalized spec without hitting the network:

```bash
python3 scripts/sync_sdk.py --skip-fetch
```

Verify that the generated sources are already up to date:

```bash
python3 scripts/sync_sdk.py --skip-fetch --check
```

Run the local build:

```bash
mvn verify
```

## Release Flow

- Daily scheduled workflow fetches the upstream OpenAPI document and opens a PR when the normalized spec or generated sources change.
- Pushing a Git tag that matches `v*` runs the publish workflow.
- Maven Central publishing and signing setup is documented in [docs/publishing.md](/Users/tianxingzhou/project/justserpapi-java/docs/publishing.md).

