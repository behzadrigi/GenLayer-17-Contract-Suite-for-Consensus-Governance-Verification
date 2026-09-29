# GenLayer Consensus Primitives Suite

A 17-contract GenLayer Intelligent Contract suite spanning 8 genuinely distinct
primitives: ambiguity-aware fact judgment with dissensus scoring, cryptographic
commit-reveal voting, semantic access control, structured proof verification,
epoch-based liveness monitoring, reputation-weighted governance, a
guarded-settlement prediction market, and multi-stage adversarial challenge
resolution.

## Why this exists

Every earlier suite on this account used one shape: register a claim, verify
it, classify it, adjust reputation. That shape works, but it is one primitive
repeated with different words. This suite instead demonstrates the range of
what GenLayer's decentralized validator consensus (the Equivalence Principle)
can do: a three-way ambiguity judgment, a majority-vote dissensus score, a
purely cryptographic commit-reveal protocol with no LLM at all, a semantic
policy check, a step-by-step proof evaluation, liveness tracked in explicit
epochs instead of wall-clock time, reputation-weighted governance voting, a
market settled by a live web-grounded oracle using internal points (never real
funds), and an escalating multi-stage challenge mechanism.

Every one of the safety lessons learned across five earlier submissions on
this account is applied throughout: identity is always bound to
`gl.message.sender_address`, never a caller-supplied parameter; no contract
ever accepts a JSON blob describing another contract's result, every
downstream read goes to the upstream contract's own on-chain state; every
non-deterministic validator independently recomputes its judgment from
scratch; every stateful action is guarded against double-application; no
contract uses `gl.block.timestamp`; and no contract holds or transfers real
funds. See [DECISIONS.md](./DECISIONS.md) for the full rationale.

## The 8 clusters

```
B. Commit-Reveal Voting (no LLM at all)
   CommitRevealVote -> CommitRevealResolver

A. Ambiguity-Aware Judgment & Dissensus
   AmbiguityOracle -> DissensusScorer

C. Semantic Access Control
   SemanticAccessGate -> AccessAuditLog

D. Structured Proof Verification
   ProofRegistry -> StructuredProofChecker

E. Epoch-Based Liveness Monitoring
   ServiceHeartbeatMonitor -> LivenessReputationLink

F. Reputation-Weighted Governance
   ProposalRegistry -> WeightedVoting (reads LivenessReputationLink) -> ProposalExecutor

G. Guarded-Settlement Prediction Market (internal points, never real GEN)
   PredictionMarket <-> MarketOracleSettlement

H. Multi-Stage Adversarial Challenge
   ChallengeableAssertion -> ChallengeOutcomeLedger
```

Each contract reads its upstream contract's state directly via
`gl.get_contract_at(Address(...)).view().method(...)`; nothing is ever passed
as a caller-supplied JSON blob standing in for another contract's result.

## Consensus patterns used

- **Strict equality, three-way label** — AmbiguityOracle, StructuredProofChecker,
  ChallengeableAssertion (both its stages)
- **Comparative, multi-field** — SemanticAccessGate, MarketOracleSettlement
- **No LLM / pure cryptographic commitment** — CommitRevealVote
- **Deterministic aggregation over prior consensus results** — DissensusScorer,
  ChallengeOutcomeLedger, WeightedVoting, ProposalExecutor, LivenessReputationLink

## Contracts and addresses (GenLayer Studio)

| # | Contract | Address |
|---|---|---|
| 1 | CommitRevealVote | `0xa88481C105e5d490708c834C8e8fbFf42133aE90` |
| 2 | CommitRevealResolver | `0x088457276DD013804C9655fB99CfD0C9B17d7d0C` |
| 3 | AmbiguityOracle | `0x74FDE232d4a410C07dd31f8394beAD8DE38dCF4E` |
| 4 | DissensusScorer | `0xA34b809602EA1E42F081AA36a6247A6fC7cde7bb` |
| 5 | SemanticAccessGate | `0x09bcbCCD0F128aB29ddC9228aF737D37F1623b91` |
| 6 | AccessAuditLog | `0x64d695F0a53a2ac4aa194126D744378956C4b230` |
| 7 | ProofRegistry | `0x5A81bBCD23004ad553f9caCC4de9cC5F35a9a083` |
| 8 | StructuredProofChecker | `0x188cDB8a68afA42Af3FadCEF3687452A890B9d65` |
| 9 | ServiceHeartbeatMonitor | `0x3cC830503F9E660b658f04A6131ce5826e8d8eA3` |
| 10 | LivenessReputationLink | `0xeBbe5c528854443e0aAE9eC83a4abbd075f9ea6F` |
| 11 | ProposalRegistry | `0x9e4b7Af1FcA914885856d4d931dF4faAcEF838b1` |
| 12 | WeightedVoting | `0xd4eB31737d857eB94f75b264F133B1c3e5FB191f` |
| 13 | ProposalExecutor | `0x108386Ad959881d2c3B89474B41C3cF6218DD5AD` |
| 14 | PredictionMarket | `0x878aF3a632E28cbE14E4a87e83897FD3e98DBd84` |
| 15 | MarketOracleSettlement | `0x6E69DfD4a8e8B061cB1A4cF0E134170a8f6bD035` |
| 16 | ChallengeableAssertion | `0xEd570624974Df028B0bd447526d363ad0B26c898` |
| 17 | ChallengeOutcomeLedger | `0xe552B9C3cdb79fD4F6E8D1E36973327075ba2D46` |

See [CONTRACTS.md](./CONTRACTS.md) for per-contract detail and safety
properties, and [tests/](./tests) for integration tests against the addresses
above. All 171 integration tests passed on GenLayer Studio, including every
guard-rail test expected to revert.

## Repo structure

```
contracts/    (17 files, one per contract above)
tests/        (17 files, one per contract above)
README.md
CONTRACTS.md
DECISIONS.md
LICENSE
```
