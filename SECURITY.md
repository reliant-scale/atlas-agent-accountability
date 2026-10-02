# Security

## Reporting

Report suspected vulnerabilities to **partnerships@reliantscale.com** with `SECURITY` in the subject. We will
acknowledge receipt. Please do not open a public issue for a suspected vulnerability.

## What this repository contains

Public interface documentation, the OpenAPI contract, examples and schemas. It contains no credentials, no
key material, no signing code, and no internal service implementation — by design.

## Properties relevant to a security reviewer

- **Fails closed.** No credential, no service. Every request re-reads the credential's state.
- **Revocation on the very next request.** There is no session and no cache, so revocation does not wait for a
  token lifetime to expire.
- **Credential stored as a hash.** The service does not hold the presented secret.
- **Unknown and revoked are indistinguishable** in the refusal, so neither reveals which credentials existed.
- **Cross-tenant reads return 404, not 403**, so existence is not confirmed to a stranger.
- **Records outlive credentials.** Revocation and termination end access, never the account of what was done.
- **Bodies are bounded**; oversized requests are refused.

## What we do not claim

We hold no SOC 2, ISO 27001, HIPAA or FedRAMP attestation, and Atlas is not a compliance certification for any
regulation. See [CLAIMS.md](./CLAIMS.md).
