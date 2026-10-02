# Credentials

A scoped, revocable bearer credential. Not OAuth2, not a JWT.

Stored as a hash and **re-read on every request**, which is what makes revocation effective on the very next
call rather than at the end of a token lifetime.

## Scopes are an upper bound, not a grant

`GET /v1/atlas/whoami` returns the principal, its organisation, and the scopes on the presented credential.

Those scopes bound what the credential may *attempt*. Whether a specific action is authorised is evaluated
separately, per action, and the evaluation is recorded in the receipt.

## Unknown and revoked are indistinguishable

Both are refused with identical text. Neither teaches an attacker which credentials once existed.

## Cross-tenant reads return 404

A receipt belonging to another organisation returns `404`, not `403`. A `403` would confirm the record exists to
someone not entitled to know that.

## Issuance

Credentials are opened by Reliant Scale with the customer. There is no public signup, no self-service issuance,
and none is created by reading this repository.
