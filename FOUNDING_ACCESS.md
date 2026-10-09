# Bring Your Agent to Atlas

**Production-backed infrastructure for AI accountability, evidence intelligence, and governed agent operations.**

Reliant Scale Technologies is accepting technical access requests from agent developers, development teams, and
organizations working on consequential AI systems.

Start with the system. No sales presentation is required.

Bring one agent, one consequential workflow, or one evidence problem. RST will determine which Atlas capabilities
apply now, what requires a controlled qualification, and what remains unsupported.

## What teams can explore

### AI accountability

Examine what an agent did, what it relied on, what it was allowed to do, what happened afterward, and whether the
event can be reconstructed. The four-operation Agent Accountability API is live as a controlled pilot surface.

### Atlas Evidence Check

Use the Atlas Evidence Engine to determine what supplied evidence supports, where it conflicts or contradicts, what
is stale, and what remains unresolved. The first access boundary uses RST-supplied synthetic evidence so teams can
exercise the capability without exposing customer production data.

### VBI and evidence intelligence

Submit a cross-system evidence question for qualification. VBI work is handled through a controlled engagement and
is not automatically included in a Founding Access grant.

### Atlas Vantage Horizon

Bring one enterprise workflow for a read-only demonstration candidate showing how Atlas can project support,
conflict, missing evidence, authority, and change across existing systems. Vantage Horizon is an enterprise
demonstration treatment, not an audit, certification, or standalone product SKU.

## How Founding Access works

```text
YOUR AGENT / DEVELOPMENT TEAM
            ↓
one consequential workflow or evidence need
            ↓
RST capability intake
            ↓
SUPPORTED NOW / QUALIFICATION REQUIRED / CAPABILITY GAP CANDIDATE
            ↓
bounded technical access or the appropriate controlled engagement
```

Every request receives one of these dispositions:

- `SUPPORTED_NOW`
- `QUALIFICATION_REQUIRED`
- `CAPABILITY_GAP_CANDIDATE`
- `OUT_OF_SCOPE`
- `PROHIBITED`
- `DUPLICATE_EXISTING_NEED`

A capability-gap request is market evidence. It does not automatically authorize a feature, expand an agent's
authority, or change the 1V core.

## Send your requirement

Use the machine-readable [`capability-request` schema](./schemas/capability-request.json) and
[example request](./examples/json/capability-request.json), or include the same information in an email to
[partnerships@reliantscale.com](mailto:partnerships@reliantscale.com?subject=Bring%20Your%20Agent%20to%20Atlas):

1. the exact question or operation your agent needs to handle;
2. the evidence types and systems involved;
3. the workflow that will consume the result;
4. the authority the agent already has;
5. the authority it must never receive;
6. the expected frequency and consequence of the decision; and
7. the Atlas path you want to explore, or `UNSURE`.

Do not send credentials, tokens, personal records, customer books, restricted information, or production data.
Sending a request does not create a credential, entitlement, charge, customer account, production permission, or
commitment to build a requested capability.

## Current access state

- Request intake is open.
- The founding synthetic evidence set has been admitted at RST HQ.
- Governed artifacts and application code are live behind a private production gate with billing disabled.
- The private production canary passed 19 of 19 checks, including entitlement, evidence states, authority-field
  refusal, idempotent retry, zero credit movement, and teardown.
- The Gate G candidate passed 12 of 12 off-production checks. Its production deployment, terms disposition, and
  Founder opening Gate H remain before external Founding Access credentials can be issued.
- RST is seeking 10 serious requests and will begin with a first activation cohort of 3 organizations after Gate H.
- Paid agent commerce remains inactive.

## The first trust boundary

The starting environment uses synthetic evidence. Results concern that evidence only and are not findings about the
participant's business.

Access is organization-granted, bounded, and revocable. An Atlas Evidence Check has `execution_authority: NONE`.
Founding Access cannot grant an agent authority to modify an external system, move money, or act for an organization.

This is controlled founding access to production-backed capability. It is not public self-service access.

**Bring your agent. Bring the workflow. Let the evidence establish what comes next.**
