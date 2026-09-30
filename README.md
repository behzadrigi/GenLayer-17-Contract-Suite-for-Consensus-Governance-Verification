# GenLayer Multi-Domain Contract Collection

A 17-contract GenLayer Intelligent Contract collection covering 8 separate
domains: cryptographic commit-reveal voting, fact verdict judgment with a
disagreement metric, policy-based access evaluation, structured proof
checking, epoch-based service liveness, reputation-weighted governance, a
points-based prediction market with web-grounded settlement, and multi-stage
adversarial challenge resolution.

## Why this exists

Earlier work on this account used one repeated shape: register a claim,
verify it, classify it, adjust reputation. This collection instead spans
several unrelated problem domains, each solved with the GenVM primitive that
actually fits it — some need decentralized LLM judgment, one needs none at
all.

Every safety lesson learned across five earlier submissions on this account
is applied throughout: identity is always bound to
`gl.message.sender_address`, never a caller-supplied parameter; no contract
ever accepts a JSON blob describing another contract's result — every
downstream read goes to the upstream contract's own on-chain state; every
non-deterministic validator independently recomputes its judgment from
scratch rather than trusting a leader's label; every stateful action is
guarded against double-application; no contract uses `gl.block.timestamp`;
and no contract holds or transfers real funds. See
[DECISIONS.md](./DECISIONS.md) for the full rationale.

## The 8 domains

```
1. Commit-Reveal Voting (cryptographic, no LLM)
   CommitRevealVote -> CommitRevealResolver

2. Fact Verdicts & Disagreement
   FactVerdictOracle -> DissensusScorer

3. Policy-Based Access Evaluation
   PolicyEvidenceGate -> AccessAuditLog

4. Structured Proof Checking
   ProofRegistry -> StructuredProofChecker

5. Epoch-Based Liveness Monitoring
   ServiceHeartbeatMonitor -> LivenessReputationLink

6. Reputation-Weighted Governance
   ProposalRegistry -> WeightedVoting (reads LivenessReputationLink) -> ProposalExecutor

7. Points-Based Prediction Market
   PredictionMarket <-> MarketOracleSettlement

8. Multi-Stage Adversarial Challenge
   ChallengeableAssertion -> ChallengeOutcomeLedger
```

Each contract reads its upstream contract's state directly via
`gl.get_contract_at(Address(...)).view().method(...)`; nothing is ever passed
as a caller-supplied JSON blob standing in for another contract's result.

## Consensus mechanisms used

GenLayer's Equivalence Principle lets independent validators agree on a
non-deterministic result. This collection uses it three different ways, plus
one contract that uses no LLM/consensus at all:

- **Three-way strict-label matching** — FactVerdictOracle, StructuredProofChecker,
  and ChallengeableAssertion each require validators to independently
  reach the exact same label from a small fixed vocabulary (e.g.
  TRUE/FALSE/AMBIGUOUS).
- **Multi-field comparison** — PolicyEvidenceGate and MarketOracleSettlement
  require validators to independently agree on every one of several fields,
  not just a single summary status.
- **Pure cryptographic commitment, no LLM** — CommitRevealVote verifies a
  reveal by exact hash comparison; correctness doesn't depend on model
  agreement at all.
- **Deterministic aggregation over already-consensed results** —
  DissensusScorer, ChallengeOutcomeLedger, WeightedVoting, ProposalExecutor,
  and LivenessReputationLink each read and combine outputs that were already
  finalized by consensus elsewhere; they add no further LLM calls of their
  own.

## Contracts and addresses (GenLayer Studio)

| # | Contract | Address |
|---|---|---|
| 1 | CommitRevealVote | `0xa88481C105e5d490708c834C8e8fbFf42133aE90` |
| 2 | CommitRevealResolver | `0x088457276DD013804C9655fB99CfD0C9B17d7d0C` |
| 3 | FactVerdictOracle | `0x74FDE232d4a410C07dd31f8394beAD8DE38dCF4E` |
| 4 | DissensusScorer | `0xA34b809602EA1E42F081AA36a6247A6fC7cde7bb` |
| 5 | PolicyEvidenceGate | `0x09bcbCCD0F128aB29ddC9228aF737D37F1623b91` |
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
properties, and [tests/](./tests) for integration tests against the
addresses above. All 171 integration tests passed on GenLayer Studio,
including every guard-rail test expected to revert.

## Repo structure

```
contracts/    (17 files, one per contract above)
tests/        (17 files, one per contract above)
README.md
CONTRACTS.md
DECISIONS.md
LICENSE
```
