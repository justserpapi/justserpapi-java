# Publishing Setup

The release workflow publishes this SDK to Maven Central through Sonatype Central Portal and creates a GitHub Release for the pushed tag.

## Required GitHub Secrets

- `MAVEN_CENTRAL_USERNAME`: Central Portal token username
- `MAVEN_CENTRAL_PASSWORD`: Central Portal token password
- `MAVEN_GPG_PRIVATE_KEY`: ASCII-armored private key used to sign artifacts
- `MAVEN_GPG_PASSPHRASE`: passphrase for the private key

## One-Time Maven Central Preparation

1. Claim and verify the `com.justserpapi` namespace in Sonatype Central Portal.
2. Create a Central Portal publishing token.
3. Export a GPG private key in ASCII-armored form.
4. Add the secrets above to the GitHub repository.

## Release Procedure

1. Merge any pending OpenAPI sync PR.
2. Update `pom.xml` to the intended release version.
3. Update `CHANGELOG.md`.
4. Commit the release metadata changes.
5. Create and push a matching tag, for example `v0.1.0`.
6. Push a matching tag, or use the `Release` workflow's manual dispatch with an existing tag after secrets are configured.
7. The `release.yml` workflow will run `mvn -Prelease deploy` and create the GitHub Release once Central publishing succeeds.

## Local Dry Run

```bash
python3 scripts/sync_sdk.py --skip-fetch --check
python3 -m unittest discover -s scripts/tests
mvn verify
```
