# Contracts

## Domain 1 — Commit-Reveal Voting

### 1. CommitRevealVote

**Pattern:** fully deterministic, no LLM at all — pure cryptographic
commitment.

**Purpose:** a two-phase commit-reveal poll. Voters first commit
`sha256(choice:salt)`, then reveal the plaintext choice and salt once the
creator advances the poll; the contract verifies the hash before counting the
vote.

**Public methods:** `create_poll`, `commit_vote`, `advance_to_reveal`,
`reveal_vote`, `close_poll`, `get_poll_status`, `get_poll_data`, `get_tally`,
`get_commitment_status`, `list_polls`.

**Safety properties**
- A vote only counts if its revealed `(choice, salt)` hashes to exactly the
  committed value — nobody can change their vote after seeing others reveal.
- One commitment per voter per poll; one reveal per commitment.
- Only the poll's creator can advance phases or close it.
- `close_poll` requires at least one reveal and picks the option with the
  highest tally as winner.

### 2. CommitRevealResolver

**Pattern:** fully deterministic — reads `CommitRevealVote`'s own on-chain
state and layers a quorum requirement on top.

**Purpose:** finalizes a closed poll's outcome only if enough voters actually
revealed, and records it permanently.

**Safety properties**
- `winner` and `total_revealed` are read directly from `CommitRevealVote`,
  never supplied by the caller.
- A poll can only be finalized once (`assert poll_id not in
  self.finalized_polls`).
- Finalization reverts outright if the observed `total_revealed` is below the
  caller-declared `min_reveals` — this is a quorum check, not a trust
  decision, since the underlying tally itself is already authenticated.

---

## Domain 2 — Fact Verdicts & Disagreement

### 3. FactVerdictOracle

**Pattern:** non-deterministic, strict equality on a three-way label
(`TRUE` / `FALSE` / `AMBIGUOUS`).

**Purpose:** judges whether a statement is true, false, or genuinely
ambiguous/unclear according to one live source — deliberately allowing "I
can't tell" as a first-class answer rather than forcing a binary call.

**Safety properties**
- The contract itself fetches `source_url` via `gl.nondet.web.render`; the
  statement is never judged from caller-supplied text alone.
- `judge_question` can only be called once per question; the record is only
  written after independent validators agree on the exact label.
- A fetch failure or empty page always resolves to `AMBIGUOUS`, never to a
  false `TRUE`/`FALSE`.

### 4. DissensusScorer

**Pattern:** fully deterministic — aggregates multiple already-authenticated
`FactVerdictOracle` judgments.

**Purpose:** assembles a panel of judgments on the *same* statement (from
different sources) and computes how much they disagreed.

**Safety properties**
- Every judgment in a panel is read from `FactVerdictOracle`'s own state and
  must share the exact same `statement` text — a panel can't silently mix
  judgments of different claims.
- Every question in the panel must already be `JUDGED`; scoring a panel that
  includes a still-`PENDING` question reverts outright rather than treating
  it as a data point.
- A given exact set of question ids can only be scored once (order-independent,
  sorted before hashing into the dedup key).
- `dissensus_score = 100 - (max_count * 100 // total)`: 0 means unanimous,
  higher means more disagreement; `majority_label` is `"SPLIT"` when there is
  no unique plurality.

---

## Domain 3 — Policy-Based Access Evaluation

### 5. PolicyEvidenceGate

**Pattern:** non-deterministic, comparative, two-field.

**Purpose:** grants or denies access to a registered resource based on
whether a requester's submitted evidence page genuinely demonstrates that
they meet the resource's stated policy.

**Safety properties**
- The contract fetches the requester's `evidence_url` itself; access is never
  granted on the strength of a claim the requester typed in.
- Access requires *both* `meets_policy` and `evidence_relevant` to be true —
  a page that's on-topic but doesn't actually satisfy the policy, or a page
  that's irrelevant filler, both correctly deny access.
- Every validator independently re-fetches and re-judges both fields; a
  mismatch on either field rejects the leader's result.
- A request can only be decided once; an already-granted agent cannot
  request the same resource again.

### 6. AccessAuditLog

**Pattern:** fully deterministic — reads `PolicyEvidenceGate`'s own decisions.

**Purpose:** a permanent, queryable audit trail of every access decision
(granted or denied).

**Safety properties**
- `decision` and `requester` are read from `PolicyEvidenceGate`'s state,
  never supplied by the caller of `record_decision`.
- A still-`PENDING` request cannot be logged; a request can only be logged
  once.

---

## Domain 4 — Structured Proof Checking

### 7. ProofRegistry

**Pattern:** fully deterministic.

**Purpose:** entry gate for a proof submission — a statement plus a URL to a
written argument for it.

**Safety properties**
- `author` is always `gl.message.sender_address`.
- An unparseable `proof_url` or empty `statement` always reverts.

### 8. StructuredProofChecker

**Pattern:** non-deterministic, strict equality on a three-way verdict
(`VALID` / `INVALID` / `INCOMPLETE`).

**Purpose:** fetches the written proof live and judges whether it correctly
and completely proves the registered statement.

**Safety properties**
- `statement` and `proof_url` are read from `ProofRegistry`'s own state.
- A fetch failure or empty page always resolves to `INCOMPLETE`, never
  `VALID`.
- `check_proof` can only be called once per proof; independent validators
  must agree on the exact verdict.

---

## Domain 5 — Epoch-Based Liveness Monitoring

### 9. ServiceHeartbeatMonitor

**Pattern:** fully deterministic. No LLM, and deliberately no
`gl.block.timestamp` (which does not exist in this SDK version) — liveness is
measured in explicit epochs that only the deploying admin can advance.

**Purpose:** tracks whether registered services/agents check in every epoch.

**Safety properties**
- Registering counts as the first heartbeat; a service can only register
  once.
- At most one heartbeat per service per epoch.
- Only the deployer can call `advance_epoch`; advancing closes the current
  epoch, and any service that didn't beat in it has `total_missed`
  incremented — two consecutive missed epochs marks it `DOWN`, and a beat in
  the next epoch clears `consecutive_missed` and restores `ACTIVE`.

### 10. LivenessReputationLink

**Pattern:** fully deterministic — reads `ServiceHeartbeatMonitor`'s own
state and converts an uptime ratio into a reputation change.

**Safety properties**
- `total_beats`/`epochs_observed` are read from the monitor's own state,
  never supplied by the caller.
- Requires at least 3 observed epochs before any reputation change can be
  applied, so a single lucky or unlucky epoch can't swing reputation.
- A given observation count for a given agent can only be applied once
  (`applied[f"{agent}:{observed}"]`) — as more epochs accumulate, the same
  agent can be re-evaluated with a fresh observation count.
- No `initialize` method: `self.reputation.get(agent, u256(50))` supplies a
  lazy default, removing any race to claim an agent's starting reputation.
- A change smaller than 10 points reverts (`"Change too small to apply"`)
  rather than being silently applied.

---

## Domain 6 — Reputation-Weighted Governance

### 11. ProposalRegistry

**Pattern:** fully deterministic.

**Purpose:** entry gate for a governance proposal.

**Safety properties:** `proposer` is always `gl.message.sender_address`;
empty title/description always reverts.

### 12. WeightedVoting

**Pattern:** fully deterministic — reads both `ProposalRegistry` and
`LivenessReputationLink` on-chain.

**Purpose:** lets addresses vote FOR/AGAINST a proposal, weighted by their
reputation above the 50-point baseline (read live from
`LivenessReputationLink`, so voting power reflects real, earned standing —
not a token balance anyone can buy).

**Safety properties**
- Only the proposal's own proposer (read from `ProposalRegistry`, not the
  caller) can open or close its voting window.
- One vote per address per proposal; a fresh address with baseline
  reputation has exactly zero voting power and reverts with `"No voting
  power"` rather than silently casting a zero-weight vote.
- `close_voting` requires at least one vote to have been cast.

### 13. ProposalExecutor

**Pattern:** fully deterministic — reads `WeightedVoting`'s own state and
adds a quorum check.

**Safety properties**
- `for_weight`/`against_weight` are read from `WeightedVoting`'s own state.
- Voting must be `CLOSED` before execution; a proposal can only be executed
  once; the combined weight must meet a caller-declared quorum or execution
  reverts.
- Outcome is a pure function of the two weights (`PASSED` iff
  `for_weight > against_weight`).

---

## Domain 7 — Points-Based Prediction Market

### 14. PredictionMarket

**Pattern:** fully deterministic. Runs entirely on an internal points ledger
(a one-time 100-point faucet per address) — it never holds, accepts, or
transfers real GEN, which avoids the whole class of fund-custody risk that
caused repeated Action Needed/Rejected cycles on an earlier escrow-style
project on this account.

**Purpose:** a YES/NO prediction market with pooled, proportional payouts.

**Safety properties**
- `set_oracle` is a one-time, deployer-only setter (resolves the circular
  deploy dependency with `MarketOracleSettlement`); every subsequent
  settlement is pinned to that address, never a caller-supplied one.
- Betting requires a sufficient real balance in the internal ledger; a
  market can't be bet on once closed.
- `settle_market` requires the market to be `CLOSED` and requires a real
  resolution to already exist in the oracle contract.
- `claim_winnings` is idempotent per address per market
  (`claimed[f"{market_id}:{agent}"]`) and pays out proportionally to stake
  within the winning pool; an `UNRESOLVED` outcome refunds every stake
  exactly rather than picking a side arbitrarily.

### 15. MarketOracleSettlement

**Pattern:** non-deterministic, comparative, two-field, web-grounded —
structurally the same rigor as `PolicyEvidenceGate`, applied to real-world
market resolution instead of an access decision.

**Safety properties**
- The contract fetches the market's own `source_url` itself; a market's
  question is never resolved from a caller's assertion.
- `resolve_market` can only be called once per market and only once the
  market is `CLOSED`.
- An unfetchable source resolves to `UNRESOLVED` (triggering a full refund
  in `PredictionMarket`) rather than defaulting to a guessed side.

---

## Domain 8 — Multi-Stage Adversarial Challenge

### 16. ChallengeableAssertion

**Pattern:** non-deterministic, strict equality, used at two different
stages with two different label sets (`SUPPORTED`/`UNSUPPORTED` for the
initial evaluation, `SUPPORTED`/`OVERTURNED` for each challenge round) —
reusing the multi-stage escalation shape from an earlier accepted project on
this account (`DisputeEscalation`), now generalized to any evidence-backed
assertion.

**Purpose:** an assertion is first evaluated against its own evidence; once
accepted, anyone but the original asserter can challenge it with
counter-evidence, escalating through up to 3 stages before finalizing.

**Safety properties**
- The contract fetches both the original evidence and any counter-evidence
  itself.
- The asserter can never challenge their own assertion; each new challenge's
  counter-evidence must differ from both the original evidence and the
  immediately preceding counter-evidence, preventing a trivial repeat
  challenge.
- Only an `ACCEPTED` assertion within the stage limit can be challenged;
  once a challenge is `OVERTURNED` or the stage limit is reached, the
  assertion reaches a terminal `FINALIZED_*` status and can never be
  challenged again.

### 17. ChallengeOutcomeLedger

**Pattern:** fully deterministic — reads `ChallengeableAssertion`'s own
terminal state.

**Purpose:** a permanent record of every assertion's final outcome and a
running upheld/lost tally per asserter.

**Safety properties**
- `final_status` must already be one of the terminal statuses
  (`FINALIZED_ACCEPTED`, `FINALIZED_OVERTURNED`, `REJECTED`); an assertion
  still `PENDING`, `ACCEPTED`, or `CHALLENGED` cannot be recorded.
- An assertion's outcome can only be recorded once.
