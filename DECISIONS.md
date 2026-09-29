# Design Decisions

## Why 8 genuinely different primitives instead of one repeated shape

Every earlier suite on this account (registry → verify → classify →
reputation) scored acceptance but few points. The reference full-score
submission for this campaign (Penumbra, 20 contracts) demonstrated breadth:
distinct primitives, not one shape re-skinned. This suite deliberately covers
territory none of the earlier suites touched: pure cryptographic
commit-reveal with no LLM, a three-way ambiguity judgment with a dissensus
metric, semantic policy evaluation, structured proof checking, epoch-based
liveness, reputation-weighted governance, a guarded prediction market, and
multi-stage adversarial challenge.

## Why CommitRevealVote uses no LLM at all

Every earlier submission on this account used the Equivalence Principle for
every consensus decision. Commit-reveal is a genuinely different kind of
decentralized coordination — cryptographic, not judgment-based — and
including it demonstrates that this account's work isn't only "wrap an LLM
call in a validator function." The correctness of a reveal is checked by
exact hash comparison, which every node computes identically; no
non-determinism is needed or introduced.

## Why AmbiguityOracle has a first-class AMBIGUOUS outcome

A strict TRUE/FALSE forced choice pushes genuinely unclear cases toward an
arbitrary answer, which independent validators are less likely to agree on
by chance — and which is simply less honest. Allowing AMBIGUOUS as a first-
class, equally-valid label (with an empty/unfetchable source defaulting to
it) makes consensus both more meaningful and more reliably reproducible.

## Why the market runs on internal points instead of real GEN

An earlier escrow-style project on this account went through repeated Action
Needed/Rejected cycles over `payable` methods, and the account's testing
setup (mobile-constrained) made verifying real value-transfer especially
slow. A prediction market is a natural fit for real funds conceptually, but
none of that risk is necessary to demonstrate the primitive itself — pooled,
proportional, oracle-gated settlement works identically over an internal
ledger. `PredictionMarket` never calls anything resembling a payable method
or a cross-contract value transfer.

## Why ServiceHeartbeatMonitor uses explicit epochs, not timestamps

`gl.block.timestamp` does not exist in this GenLayer SDK version (confirmed
by a runtime `AttributeError` on an earlier project). Liveness is
conceptually about "did you check in recently," which time-based logic would
naturally express — but an explicit, admin-advanced epoch counter expresses
the same guarantee without depending on an unavailable API, and is arguably
more deterministic besides (every validator agrees on the current epoch by
construction, with no clock skew to reason about).

## Why WeightedVoting reads voting power from a reputation contract instead of a token balance

A token-weighted vote can be bought by anyone willing to spend; reading
`LivenessReputationLink`'s earned reputation instead means voting power
reflects a track record the address actually built by being reliably live,
not capital. This also demonstrates genuine cross-primitive composition —
Cluster F depends on Cluster E's output, not just a copy of its shape.

## Why every downstream contract reads on-chain state instead of accepting JSON

A submission on this account was rejected specifically because downstream
scoring/reputation contracts trusted a JSON string supplied by the caller
instead of the verifying contract's own authenticated output. Every one of
the 17 contracts here that depends on another reads it directly via
`gl.get_contract_at(Address(...)).view().method(...)`. None accept a
caller-supplied JSON blob standing in for another contract's result.

## Why identity is always `gl.message.sender_address`, never a parameter

A related earlier gap: even after contracts started reading real on-chain
data, an identity field was still sometimes accepted as a caller-supplied
parameter, which let a legitimate result be paired with an unrelated agent.
Every "who did this" field in this suite — `agent`, `asker`, `author`,
`proposer`, `requester`, `asserter`, `challenger` — is captured exactly once,
from the real transaction sender, at the point of the original action, and
threaded through every downstream read from there.

## Why every non-deterministic contract's validator recomputes fully

An earlier submission was rejected because a validator checked only that a
leader's status label was one of the allowed values, without independently
recomputing the data that produced it. Every validator across all 8 clusters
— whether checking a three-way label, a two-field comparison, or a numeric
tally — independently redoes the underlying fetch and judgment from scratch
and only accepts the leader's result if its own computation matches.

## Why every stateful action is guarded against double-application

Every write method that changes durable state checks a membership/boolean
map before doing any work, and only marks that map after a fully successful
run — so a reverted attempt never "consumes" the record it was processing.
This closes the exact gap from an earlier rejection where a scoring contract
could permanently mark a still-unfinished verification as scored.

## Why helper logic lives in module-level functions, not undecorated instance methods

GenLayer Studio fails to load a contract's schema if a `gl.Contract`
subclass has any plain instance method without a `@gl.public.write` or
`@gl.public.view` decorator. Every one of the 17 contracts was checked
programmatically (not just by eye) to confirm zero undecorated instance
methods before deployment; all shared logic (URL cleaning/validation, label
parsing, yes/no prompting, hash computation) lives in module-level
functions.
