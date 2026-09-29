# TESTS

GenLayer Penumbra-Scale Suite: 17 contracts, 171 integration tests, all run on GenLayer Studio.

Explorer base: `https://explorer-studio.genlayer.com/tx/<tx_hash>`

Rows marked "read-only call" are view calls with no transaction, so there is no link.

---

## Section 1: Deployed Contracts (17)

| # | Contract | Address |
|---|----------|---------|
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

---

## Section 2: Deploy Transactions (17)

| # | Contract | Deploy Tx |
|---|----------|-----------|
| 1 | CommitRevealVote | [0xc45d…77f0](https://explorer-studio.genlayer.com/tx/0xc45d5cd5d892a5f161eece012390674c72f5a91805087ecf13bfac781c9b77f0) |
| 2 | CommitRevealResolver | [0xbd45…48e9](https://explorer-studio.genlayer.com/tx/0xbd45d802d52a8059465e2c144777ddc23149b22a4e6652ebe807e6624d6048e9) |
| 3 | AmbiguityOracle | [0xa6c4…c34b](https://explorer-studio.genlayer.com/tx/0xa6c47a653f06091e71425f9d720635f6fa0419b9c7d24cb7e9edf646060ac34b) |
| 4 | DissensusScorer | [0x8304…4099](https://explorer-studio.genlayer.com/tx/0x8304aa2d50114d7ca367d253dc3e4d906b7c921ce6b5ab29c376eedacf634099) |
| 5 | SemanticAccessGate | [0xf2e8…06f4](https://explorer-studio.genlayer.com/tx/0xf2e829ff2671b77ce3f2cd3882874a0ba3a698bdb21f66029565eeb9a0fd06f4) |
| 6 | AccessAuditLog | [0xc051…aca8](https://explorer-studio.genlayer.com/tx/0xc051245d910780290c64d8b1ebb24fa01f73955d7c29e54f5da0bbe80eccaca8) |
| 7 | ProofRegistry | [0xa54b…4dca](https://explorer-studio.genlayer.com/tx/0xa54b3946de008522acacea5a3007ef87ead180570785e212626d6e3468674dca) |
| 8 | StructuredProofChecker | [0xca7a…cbbc](https://explorer-studio.genlayer.com/tx/0xca7a724a15826b12af8634931db4ee09f0b67e8dfd69c3906b3f80226e6ecbbc) |
| 9 | ServiceHeartbeatMonitor | [0xf219…7b5e](https://explorer-studio.genlayer.com/tx/0xf21914aaa02419a04fc3545d9e7a67c52925a0a744575e1cbe7037f8be8d7b5e) |
| 10 | LivenessReputationLink | [0xa689…6625](https://explorer-studio.genlayer.com/tx/0xa68905a63bd211c3141fc250bd7814e2e5df7bb587578fdd6ae311c26c0d6625) |
| 11 | ProposalRegistry | [0x1e04…a11e](https://explorer-studio.genlayer.com/tx/0x1e04db5d5a33e75766cfe0689d9b20cf5b5a35191bc01e97d5c50bfb977fa11e) |
| 12 | WeightedVoting | [0xb4ce…7cac](https://explorer-studio.genlayer.com/tx/0xb4ce0c9cc8500f32e2e612256de3e9054f9344cceea50b6113813ede55267cac) |
| 13 | ProposalExecutor | [0xe6ba…3ecc](https://explorer-studio.genlayer.com/tx/0xe6ba4840d704eb3fef833cab0bdbbb08174142a2efbae2018b40ff630e0e3ecc) |
| 14 | PredictionMarket | [0xde29…89f2](https://explorer-studio.genlayer.com/tx/0xde29be320f479d6e0b2a377e8f2656eee777198cec4a212856d1deaa337089f2) |
| 15 | MarketOracleSettlement | [0x2379…f54c](https://explorer-studio.genlayer.com/tx/0x2379a54e8efe0e2b95d76b430ea0497729f7510a3f9ef8315203fa782a6af54c) |
| 16 | ChallengeableAssertion | [0xe398…c17f](https://explorer-studio.genlayer.com/tx/0xe398074592d95e55cc7dbe519443db8ec781eebca0a8697ed74d799845b4c17f) |
| 17 | ChallengeOutcomeLedger | [0xf62d…6d28](https://explorer-studio.genlayer.com/tx/0xf62d4a697aaed452fb25544ca4a4032e82d2a6c51834567f957f51e775cc6d28) |

---

## Section 3: Test Transactions by Cluster

Roles: A, B, C are three separate test accounts.

### Cluster B: CommitRevealVote + CommitRevealResolver

Tests: 24

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| CR1 | `create_poll("Should we merge PR 42?", "YES,NO")` as A. Success, PID_1 = 0 | [0x50ce…9893](https://explorer-studio.genlayer.com/tx/0x50ce9090ff0f5d9a63932080a39f357cd0772e1073e7d0ac6b26aa486bfd9893) |
| CR2 | `create_poll("q", "YES,YES")`. Reverts: "Duplicate options" | [0xc982…a0e9](https://explorer-studio.genlayer.com/tx/0xc982933179be78aac7092743b43d3f86a654e65274305b5250305c2921e3a0e9) |
| CR3 | `create_poll("q", "YES")`. Reverts: "At least 2 options required" | [0xb19f…fa5c](https://explorer-studio.genlayer.com/tx/0xb19f325109516a48798aed0a0cc4546390a2e578c3dfe0cf960deca86e85fa5c) |
| CR4 | `commit_vote(PID_1, sha256("YES:saltA"))` as A. Success | [0x2be4…82bb](https://explorer-studio.genlayer.com/tx/0x2be4920489b154e6d631c04c5f8aab5c23f27e09fa5ab3f0a0e9980e73d482bb) |
| CR5 | `commit_vote(PID_1, sha256("NO:saltB"))` as B. Success | [0xc415…eb98](https://explorer-studio.genlayer.com/tx/0xc415c3f8c089819c55d2844e3adbc162b537c1980924e9331e06aa797139eb98) |
| CR6 | `commit_vote(PID_1, sha256("YES:saltC"))` as C. Success | [0x49c9…5156](https://explorer-studio.genlayer.com/tx/0x49c96538b306aa76133c9e3a453a889f63c2738196dcb30e8ba93ab9b54d5156) |
| CR7 | `commit_vote` as A again. Reverts: "Already committed to this poll" | [0x076c…d9ce](https://explorer-studio.genlayer.com/tx/0x076c30bf1853f3cac72a970b647a0ae6f0b8e38c2d445a9fdbe7b116a105d9ce) |
| CR8 | `reveal_vote(PID_1, "YES", "saltA")` as A during commit phase. Reverts: "Poll is not in reveal phase" | [0x8efa…bb2a](https://explorer-studio.genlayer.com/tx/0x8efa3963251364b83e4d47060911106904128c04ba8b58689d6f6a31d0cabb2a) |
| CR9 | `advance_to_reveal(PID_1)` as B. Reverts: "Only creator can advance the poll" | [0x4325…c243](https://explorer-studio.genlayer.com/tx/0x43255b6e86e04dd3e084aceb6f95fa7b1eebb4cdbde28292d81b8e445fedc243) |
| CR10 | `advance_to_reveal(PID_1)` as A. Success, status REVEAL | [0xdb08…291c](https://explorer-studio.genlayer.com/tx/0xdb0802cf8f2295f5baa6be24d92979da39f3fe09df90e1c8accaf6f9bff5291c) |
| CR11 | `reveal_vote(PID_1, "NO", "wrongsalt")` as A. Reverts: "Revealed choice does not match commitment" | [0x2fba…2080](https://explorer-studio.genlayer.com/tx/0x2fba8f68c1a9bd2374909ba54f23ed1eb915fcbd24629ad0b55449af0c262080) |
| CR12 | `reveal_vote(PID_1, "YES", "saltA")` as A. Success | [0x154e…35ca](https://explorer-studio.genlayer.com/tx/0x154e3814c5484a8b8ce9ce8ccdfe86d7a05d419030aae4fc717e5ec4f56435ca) |
| CR13 | `reveal_vote` as A again. Reverts: "Already revealed" | [0x3d39…8ab1](https://explorer-studio.genlayer.com/tx/0x3d394cde1e8510051413d17a48810b43fd0b58a30025e4933fa1babeca428ab1) |
| CR14 | `reveal_vote(PID_1, "NO", "saltB")` as B. Success | [0xbf8e…4536](https://explorer-studio.genlayer.com/tx/0xbf8e4683908ee09c88a6f2e95aeec051df368f54435ee4d98cef6b7a31564536) |
| CR15 | `reveal_vote(PID_1, "YES", "saltC")` as C. Success | [0xabd8…b381](https://explorer-studio.genlayer.com/tx/0xabd83895fcc0d9e819847757c8d58b6fa90bdcd3caaf3aa934fda720fe67b381) |
| CR16 | `get_tally` for YES = "2" and NO = "1". Both correct | read-only call |
| CR17 | `close_poll(PID_1)` as B. Reverts: "Only creator can close the poll" | [0x787e…aba3](https://explorer-studio.genlayer.com/tx/0x787ec9b9f66987f600d30a82d9177563690c48e919df9c8b52e371afe2f3aba3) |
| CR18 | `close_poll(PID_1)` as A. Success, returns "YES". Poll data: status CLOSED, winner YES, total_revealed 3 | [0xc34f…c3c3](https://explorer-studio.genlayer.com/tx/0xc34f135ee53978f44df4da5cfabb625aa48abf082d7ea4f4a2dffd1927b3c3c3) |
| CR19 | `finalize_poll(PID_1, 5)`. Reverts: "Quorum not met" | [0x974a…7fe2](https://explorer-studio.genlayer.com/tx/0x974a1128a4c95f6867fe7c5d93040113534c68872212bd569697f4cef44f7fe2) |
| CR20 | `finalize_poll(PID_1, 0)`. Reverts: "min_reveals must be positive" | [0x0735…d738](https://explorer-studio.genlayer.com/tx/0x0735c765ee36747e0ac76518bb7a18a3e759ad25ee03a0671ca3262727c0d738) |
| CR21 | `finalize_poll(PID_1, 2)`. Success. Outcome: winner YES, total_revealed 3, min_reveals_required 2, status FINALIZED | [0x10df…958a](https://explorer-studio.genlayer.com/tx/0x10df72cbc1f1b36c5ca034c7bd136196ba6087e405e5feb108a39874e1e2958a) |
| CR22 | `finalize_poll(PID_1, 2)` again. Reverts: "Poll already finalized" | [0xe5c6…8cb0](https://explorer-studio.genlayer.com/tx/0xe5c6f5c57324b16a4c5922c182f1806c26d0a769925ef2bd67040a116ebb8cb0) |
| CR23 | `finalize_poll(999, 1)`. Reverts: "Poll not found in vote contract" | [0xe024…32e9](https://explorer-studio.genlayer.com/tx/0xe0249c08f051cb1056a08788ce5ab44721783ad38bcb04ba8ccdfb5ab3e732e9) |
| CR24 | Create PID_2, commit as A, then `close_poll(PID_2)` as A. Reverts: "Poll must be in reveal phase to close" | [create](https://explorer-studio.genlayer.com/tx/0xe94716d64267ab2c0617c3e3015103f1a839566a778fbead9010f82956c4651e), [commit](https://explorer-studio.genlayer.com/tx/0x34c45d418ba71b65d6538d077e111465a4e733545fbeda2b091c88bd26a6256f), [close](https://explorer-studio.genlayer.com/tx/0x67a2a878022e1984b86b52c95fa7e8d7b5d47e16f389d7b046e33a88916328ac) |

### Cluster A: AmbiguityOracle

Tests: 14

Let S = "Python was created by Guido van Rossum".

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| AM1 | `submit_statement(S, "not_a_url")`. Reverts: "Invalid source URL" | [0x9610…98f2](https://explorer-studio.genlayer.com/tx/0x96101dcc167c961d2de306d158b73372b9f0c2e4e914c22937ce1469c94298f2) |
| AM2 | `submit_statement("", wikipedia/Guido)`. Reverts: "Statement cannot be empty" | [0x28de…f6f6](https://explorer-studio.genlayer.com/tx/0x28deb3b889fbe04a1e2edbdf4609cace23675a9c5d4fdb2ed8b51c70806ef6f6) |
| AM3 | `submit_statement(S, wikipedia/Guido_van_Rossum)` as A. Success, Q0 = 0 | [0xaa0c…6e97](https://explorer-studio.genlayer.com/tx/0xaa0c8520236eed658c07e5cf0a8cb988096a5ed15424615632cccfd67d456e97) |
| AM4 | `submit_statement(S, python.org/about)`. Success, Q1 = 1 | [0xee3f…f981](https://explorer-studio.genlayer.com/tx/0xee3fcd044dd2e3cf176a3ee3347d2b46455ee4fce198c672a4b52097d815f981) |
| AM5 | `submit_statement(S, nasa.gov)`. Success, Q2 = 2 | [0x407f…4605](https://explorer-studio.genlayer.com/tx/0x407f5a8550c6cc92555b54e613f676bc51747f7a795355dc851c89084fad4605) |
| AM6 | `submit_statement("The Moon orbits the Earth", wikipedia/Moon)`. Success, Q3 = 3 | [0xd325…4722](https://explorer-studio.genlayer.com/tx/0xd325a5229bf1220a91bed3aac3040db03f72ad2cd223f06fe086a4fb663b4722) |
| AM7 | `submit_statement(S, python.org/downloads)`, left unjudged. Success, Q5 = 5 (Q4 was created by a browser auto-refresh). `list_questions` shows all six PENDING | [0xfc75…cb26](https://explorer-studio.genlayer.com/tx/0xfc7515d78e13672696eb393de46426b233e4ae65af1b21db4aa2332cbd46cb26) |
| AM8 | `get_judgment_data(Q0)`. asker = A, status PENDING, label empty | read-only call |
| AM9 | `judge_question(Q0)`. Success, label "TRUE" | [0x653a…3f85](https://explorer-studio.genlayer.com/tx/0x653aa092eb7ecedcb34670a196f4078b3ccc67da6f98e1b8dab3ebbc768a3f85) |
| AM10 | `judge_question(Q1)`. Success, label "AMBIGUOUS" | [0x7ce8…5019](https://explorer-studio.genlayer.com/tx/0x7ce8ed104a88ee2ecd412eba8899abd23a45334a7493dcc8db15fde2119a5019) |
| AM11 | `judge_question(Q2)`. Success, label "AMBIGUOUS" | [0xf70a…cd82](https://explorer-studio.genlayer.com/tx/0xf70a35e9d6d41b2afc32efac8e710a7fa12843b5eadfa8d69ab5daad4bc3cd82) |
| AM12 | `judge_question(Q3)`. Success, label "TRUE" | [0x9128…9edf](https://explorer-studio.genlayer.com/tx/0x91280e95bf1fd974f77dd30458f239f450b66839ee8727d987cf75a7096b9edf) |
| AM13 | `judge_question(Q0)` again. Reverts: "Already judged" | [0x490d…e918](https://explorer-studio.genlayer.com/tx/0x490d25e24c4cb76cac4a8b5e2d0cf7598120c7e3a2499ba64734d98ac450e918) |
| AM14 | `judge_question(999)`. Reverts: "Question not found" | [0x5288…544e](https://explorer-studio.genlayer.com/tx/0x5288231b55ab0d666ec0a356938ce8a81c17b61bf5b7d367bcb25b900ecb544e) |

### Cluster DS: DissensusScorer

Tests: 9

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| DS1 | `score_panel("0")`. Reverts: "A panel needs at least 2 judgments" | [0x6e82…dd3d](https://explorer-studio.genlayer.com/tx/0x6e82bdc7fc005a2cf1a336813e000fff85ef7399facfd85ae1223c2500f0dd3d) |
| DS2 | `score_panel("0,0")`. Reverts: "Duplicate question id in panel" | [0xe2a6…ed26](https://explorer-studio.genlayer.com/tx/0xe2a6c4fd7e7679c1faadd7cf850a2cd7cc6480c92335fa5a45a6b6f80a1fed26) |
| DS3 | `score_panel("abc")`. Reverts: "question_ids must be comma-separated integers" | [0xd598…d08d](https://explorer-studio.genlayer.com/tx/0xd5981bd4800866ad7d5e96507004d451f6d86bfd67dbab16cbc636eeaecfd08d) |
| DS4 | `score_panel("0,1,2")`. Success, panel_id = 0. true_count 1, false_count 0, ambiguous_count 2, majority_label "AMBIGUOUS", dissensus_score 34 | [0x968a…c818](https://explorer-studio.genlayer.com/tx/0x968ab0e9c651f1219e7553684650c995fb56a81fd3430908b364316d5a4cc818) |
| DS5 | `score_panel("2,1,0")`, same panel. Reverts: "Panel already scored" | [0xab01…304c](https://explorer-studio.genlayer.com/tx/0xab01459959bae37a68971477c7512958385a065e5d2c4c4956ec5d7f7741304c) |
| DS6 | `score_panel("0,3")`. Reverts: "Panel questions must share the same statement" | [0xe340…fd93](https://explorer-studio.genlayer.com/tx/0xe3409ead530524f7711d50753af4dcd45177fd92c0cfd1a4c630697a323efd93) |
| DS7 | `score_panel("0,4")`. Reverts: "Question 4 has not been judged yet" | [0x95bb…9978](https://explorer-studio.genlayer.com/tx/0x95bb664013354479b77cde8b189d92891daf026f9cb20554cdb27b8aa5979978) |
| DS8 | `score_panel("0,77")`. Reverts: "Question 77 not found in oracle" | [0x785c…b605](https://explorer-studio.genlayer.com/tx/0x785c7ff9aeacddbda823c3038f20e10b81ba694cac469189752cf66eeb13b605) |
| DS9 | `get_panel_data(0)` and `list_panels()`. `list_panels()` = "0:AMBIGUOUS:34" | read-only call |

### Cluster C: SemanticAccessGate + AccessAuditLog

Tests: 20

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| SG1 | `register_resource("Python Guild Repo", <policy: published, verifiable Python experience>)` as A. Success, R0 = 0 | [0xb560…f692](https://explorer-studio.genlayer.com/tx/0xb560c3c1b8d10e9fe98a2a1cb2427109200fc341b8b2e86cfdc58e0fad8cf692) |
| SG2 | `register_resource("", "policy")`. Reverts: "Name cannot be empty" | [0xc2f9…989e](https://explorer-studio.genlayer.com/tx/0xc2f9624907a0b7e1ed5938319e629cc334bdccae1284193142c57b6ba1cd989e) |
| SG3 | `register_resource("name", "")`. Reverts: "Policy cannot be empty" | [0xf1d5…b098](https://explorer-studio.genlayer.com/tx/0xf1d5d29cbee0ae479892bd655e0983e2f8238e47d111be0d31c02650835fb098) |
| SG4 | `request_access(R0, "not_a_url")` as B. Reverts: "Invalid evidence URL" | [0x35d9…b666](https://explorer-studio.genlayer.com/tx/0x35d9d23d017426eeb105f7b6311a8d539b06645fa1a9d93a3dbc1ef83cf9b666) |
| SG5 | `request_access(999, python.org/about)` as B. Reverts: "Resource not found" | [0x51f9…5b4a](https://explorer-studio.genlayer.com/tx/0x51f918087e14922b54ceb0338e03c9805f71f7dcb61bb62e985063e6a78f5b4a) |
| SG6 | `request_access(R0, wikipedia/Guido_van_Rossum)` as B. Success, REQ0 = 0 | [0x66a6…4765](https://explorer-studio.genlayer.com/tx/0x66a6a2959d82bdc7b35b6184d1c4a227abc544e90e0824a1cc7e1dcbb5344765) |
| SG7 | `request_access(R0, nasa.gov)` as C. Success, REQ1 = 1 | [0xb28c…6ae9](https://explorer-studio.genlayer.com/tx/0xb28ca2a1f0bac2d1e4393d13cb4c19d966dda66b7ca9d9ad0a68ae5286986ae9) |
| SG8 | `decide_access(REQ0)` as A. meets_policy true, evidence_relevant true, GRANTED | [0x2f8e…b0c8](https://explorer-studio.genlayer.com/tx/0x2f8e4077e0db41bb38034b063d39dfde033e529e21fbbf529c0c74c8da0eb0c8) |
| SG9 | `decide_access(REQ1)` as A. meets_policy false, DENIED | [0x3d89…e4ce](https://explorer-studio.genlayer.com/tx/0x3d89b27da42296d68c6826dd9a18ba52dc1554f3f2271f2597d956bfd897e4ce) |
| SG10 | `decide_access(REQ0)` again. Reverts: "Already decided" | [0xee24…b6d4](https://explorer-studio.genlayer.com/tx/0xee24352632cbc1b1576ed993a068c42129f1f1eaa11224d2ba1ff15fc161b6d4) |
| SG11 | `decide_access(999)`. Reverts: "Request not found" | [0xabe0…f7b7](https://explorer-studio.genlayer.com/tx/0xabe00a4737c46e494f19f23825b61047c21390c79c899b31832e8a78c0c4f7b7) |
| SG12 | `has_access(R0, B)` = "GRANTED"; `has_access(R0, C)` = "NO_ACCESS" | read-only call |
| SG13 | `request_access(R0, python.org/about)` as B, already granted. Reverts: "Access already granted" | [0x1af4…611d](https://explorer-studio.genlayer.com/tx/0x1af491ce1c127fdcfef45e82284d7d1ae23925ba0448f69cb33b7b3c4ece611d) |
| SG14 | `request_access(R0, python.org/about)` as C. Success, REQ2 = 2 (left undecided) | [0x3198…2d9c](https://explorer-studio.genlayer.com/tx/0x319819f4de25f65ab1da4d9975c9dde567561ca30342f18919f7e93ade062d9c) |
| AL1 | `record_decision(REQ0)` as A. Success, log_id = 0 | [0xc58c…f3f6](https://explorer-studio.genlayer.com/tx/0xc58c145966c13a7de9007eadc619eda67dd2b974845998207777381188bff3f6) |
| AL2 | `record_decision(REQ0)` again. Reverts: "Decision already logged" | [0x4d42…9fa8](https://explorer-studio.genlayer.com/tx/0x4d421519a9e711e6b09414f2a732a3d7739c3273fef9e7c4bd3ab66b8a2e9fa8) |
| AL3 | `record_decision(REQ2)`, undecided. Reverts: "Request has not been decided yet" | [0x86b3…6a0c](https://explorer-studio.genlayer.com/tx/0x86b3849992906a681a0fe9de88cf770ccabd7ffc4dcbee56ac5b9126930c6a0c) |
| AL4 | `record_decision(REQ1)`, DENIED. Success, log_id = 1 | [0x1087…5269](https://explorer-studio.genlayer.com/tx/0x1087a07e66b26df9c69a337b1b2731287d981211f72070bc7f1bf1af3c645269) |
| AL5 | `record_decision(999)`. Reverts: "Request not found in gate" | [0x2ef0…cae5](https://explorer-studio.genlayer.com/tx/0x2ef0910673fb7d4877f16e99c3627de4b0073480a767ff97347543725e9bcae5) |
| AL6 | `get_agent_logs(B)` = "0:GRANTED"; `get_agent_logs(C)` = "1:DENIED"; `get_resource_logs(0)` and `list_logs()` = "0:GRANTED,1:DENIED" | read-only call |

### Cluster D: ProofRegistry + StructuredProofChecker

Tests: 10

PS = "In a right triangle the square of the hypotenuse equals the sum of the squares of the other two sides".

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| PR1 | `submit_proof("", wikipedia/Pythagorean)`. Reverts: "Statement cannot be empty" | [0xb44e…ad1c](https://explorer-studio.genlayer.com/tx/0xb44edf8c1ab50d96db66fc97928449f465c4ce559af552e1714ec32c5d77ad1c) |
| PR2 | `submit_proof(PS, "not_a_url")`. Reverts: "Invalid proof URL" | [0x9a09…78d9](https://explorer-studio.genlayer.com/tx/0x9a096124c004314ef98f5815d092864ffc4f14877d2ba143079a29ca146978d9) |
| PR3 | `submit_proof(PS, wikipedia/Pythagorean_theorem)` as A. Success, P0 = 0 | [0x57dd…2592](https://explorer-studio.genlayer.com/tx/0x57dd63d830beaefa799ce23812034363fd8521e622b8841fc68fea05a4172592) |
| PR4 | `get_proof_data(P0)`. author = A, status SUBMITTED | read-only call |
| PR5 | `submit_proof(PS, nasa.gov)`. Success, P1 = 1 | [0x1282…e328](https://explorer-studio.genlayer.com/tx/0x1282ef32aaee0b391019a1179b1aab9ad889810786b961d0099951ab53dce328) |
| PC1 | `check_proof(P0)`. Success, verdict "INCOMPLETE" | [0x2294…e1ee](https://explorer-studio.genlayer.com/tx/0x2294aaac59988ed479b3e6220d671d085333a3d9c36c6fbed37b9365d7c2e1ee) |
| PC2 | `check_proof(P1)`. Success, verdict "INVALID" | [0x71c3…4ac8](https://explorer-studio.genlayer.com/tx/0x71c3968319fe4ad72c5d5bce701f39fb9f77ba58c07e5219802c497a31a24ac8) |
| PC3 | `check_proof(P0)` again. Reverts: "Already checked" | [0xeaa3…ccb2](https://explorer-studio.genlayer.com/tx/0xeaa361563df8f3f499455f8965242b37c21ad856224782592ef30319b01fccb2) |
| PC4 | `check_proof(999)`. Reverts: "Proof not found in registry" | [0xe4c5…3c83](https://explorer-studio.genlayer.com/tx/0xe4c57ed60ea5f95473aeaf3c5110c10b1108d6fa3f7a0e8b20ba031861553c83) |
| PC5 | `get_check_data(0)`, `list_checks()`, `get_author_proofs(A)`, `list_proofs()`. list_checks = "0:INCOMPLETE,1:INVALID" | read-only call |

### Cluster E: ServiceHeartbeatMonitor + LivenessReputationLink

Tests: 22

Epochs are advanced by hand. Epoch 0 starts at deploy.

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| E1 | `advance_epoch()` as B. Reverts: "Only admin can advance the epoch" | [0x9f07…b57c](https://explorer-studio.genlayer.com/tx/0x9f075e1cbd33df13a20e90470a6f2deb5811061ce39311f7f90b4875b703b57c) |
| E2 | `register_service("")` as B. Reverts: "Name cannot be empty" | [0x0732…cb4e](https://explorer-studio.genlayer.com/tx/0x0732e067f18febc476b427ea3a206dad81add0e606024b47f30b8d28f932cb4e) |
| E3 | `register_service("service-b")` as B. Success. total_beats 1, total_missed 0, epochs_observed 1, ACTIVE | [0x9237…1ace](https://explorer-studio.genlayer.com/tx/0x92379d43622e38e262a4e6225bece9750042f7c4bef1fba1cfe824ca57541ace) |
| E4 | `register_service("service-c")` as C. Success | [0x7f2c…68a5](https://explorer-studio.genlayer.com/tx/0x7f2c71346623d9abe8d8c85b94e6a52ac56f8671caaf99ba5dee77bf5a3e68a5) |
| E5 | `register_service("again")` as B. Reverts: "Service already registered" | [0x2391…88c7](https://explorer-studio.genlayer.com/tx/0x239125d57401451f152f2c5e37c9a701293793eef26aeea0e85170cda17d88c7) |
| E6 | `heartbeat()` as B, already beat this epoch. Reverts: "Already sent a heartbeat this epoch" | [0xee16…9f27](https://explorer-studio.genlayer.com/tx/0xee162b1fcffc1f8d111cd228af47d4f51ac164e802d30f9a6ed888ce61429f27) |
| E7 | `heartbeat()` as A, never registered. Reverts: "Service not registered" | [0x904c…6785](https://explorer-studio.genlayer.com/tx/0x904c1edfe1ccbf9cda32fd7329456dcdca47e948ab3256dbd1cc6136fea76785) |
| E8 | `apply_liveness(B)` on LivenessReputationLink. Reverts: "Not enough epochs observed" | [0x88d4…86f8](https://explorer-studio.genlayer.com/tx/0x88d489df426a3139efa0d4e5103a39e1d62c7544b1d58f8e7758411161a686f8) |
| E9 | `advance_epoch()` as A. Success. Epoch 0 closed, B and C both beat | [0xdb9d…0fe5](https://explorer-studio.genlayer.com/tx/0xdb9d9dfbf825e9cd47ce3c2e7cf7b6e07d408a45881186474cd37eb17d670fe5) |
| E10 | `heartbeat()` as B in epoch 1; C sends nothing. Success | [0x855a…dd98](https://explorer-studio.genlayer.com/tx/0x855adee22ce60091a2eadc4d0b592d2a16dd2ebe787dae84952096edf4d7dd98) |
| E11 | `advance_epoch()` as A. Success. Epoch closed, B beat, C missed | [0xd083…3223](https://explorer-studio.genlayer.com/tx/0xd0835f598bd94dcf6b247bd31647b04725ba4c9cdb6084d9a6c86f06e1a73223) |
| E12 | `get_service_data(C)`. total_missed 1, consecutive_missed 1, epochs_observed 2, ACTIVE | read-only call |
| E13 | `heartbeat()` as B in epoch 2; C sends nothing. Success | [0xb632…785f](https://explorer-studio.genlayer.com/tx/0xb6328a1c1b82ad7b80462b9302a849ed1511aba6a747de90f5fc07180a10785f) |
| E14 | `advance_epoch()` as A. Success. C missed twice in a row, status DOWN | [0xb23d…916b](https://explorer-studio.genlayer.com/tx/0xb23d4fab430cae9f0aced92782e1993ccaebe92cbbd5bf2bb128cc845d2c916b) |
| E15 | `get_service_data(C)`. DOWN, total_beats 1, total_missed 2, consecutive_missed 2, epochs_observed 3 | read-only call |
| E16 | `get_service_data(B)`. ACTIVE, total_beats 3, total_missed 0, epochs_observed 3 | read-only call |
| LR1 | `apply_liveness(A)`, A never registered. Reverts: "Service not found in monitor" | [0xa668…8e37](https://explorer-studio.genlayer.com/tx/0xa668d0cbfba282dfe695618c8d1f5bbed7f1b0a0bf25dd488f0b271c3f558e37) |
| LR2 | `apply_liveness(B)`. Success, change_id 0, uptime_score 100, INCREASE. `get_reputation(B)` = "REPUTATION:100" | [0x02bb…d90e](https://explorer-studio.genlayer.com/tx/0x02bb9f97719974c0019bcde2eb398ba23c5da05d57edcebb003de1686670d90e) |
| LR3 | `apply_liveness(B)` again. Reverts: "Already applied for this observation count" | [0x0ade…d81f](https://explorer-studio.genlayer.com/tx/0x0adeb831845467581d30b7163f3ba7cc87d9b2013e817d05ba937f898efdd81f) |
| LR4 | `apply_liveness(C)`. Success, change_id 1, uptime_score 33, DECREASE. `get_reputation(C)` = "REPUTATION:33" | [0xffb4…a00c](https://explorer-studio.genlayer.com/tx/0xffb4d9fb72cc6c1247dd9fa424a52c91de6636de581385cc158b7c7590a4a00c) |
| LR5 | `get_reputation(A)` = "REPUTATION:50" (lazy default, never initialised) | read-only call |
| LR6 | `list_changes()` = "0:INCREASE,1:DECREASE" | read-only call |

### Cluster F: ProposalRegistry + WeightedVoting + ProposalExecutor

Tests: 21

Voting power = reputation above 50. From Cluster E: B = 100 (power 50), C = 33 (power 0), A = 50 (power 0).

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| GV1 | `create_proposal("", "desc")`. Reverts: "Title cannot be empty" | [0x06d2…3fde](https://explorer-studio.genlayer.com/tx/0x06d20a0871ce9adc6c594afd2128fcbf49486f6785b727bbf76ce5564f3b3fde) |
| GV2 | `create_proposal("Adopt policy X", "Adopt the new contribution policy")` as A. Success, PROP0 = 0 | [0xd973…e58c](https://explorer-studio.genlayer.com/tx/0xd973e2beb27655c7a2a1182a638037d06ba5381b116835a889abac48b8eae58c) |
| GV3 | `open_voting(PROP0)` as B. Reverts: "Only the proposer can open voting" | [0x82e8…456c](https://explorer-studio.genlayer.com/tx/0x82e8dcf13c4eee6d79fbe656d5bae26edee2bfe684daf263c86378d2e7ca456c) |
| GV4 | `open_voting(999)` as A. Reverts: "Proposal not found in registry" | [0x1693…5ce1](https://explorer-studio.genlayer.com/tx/0x169324b653c8f9f8873c24905d682097896d9d2f049876efc60c6a3ae1095ce1) |
| GV5 | `open_voting(PROP0)` as A. Success | [0xb22a…5cf3](https://explorer-studio.genlayer.com/tx/0xb22a9feab6ab4042ae14714a130cfad2bb261b9d4e7fb45dc11c7047e3225cf3) |
| GV6 | `open_voting(PROP0)` as A again. Reverts: "Voting already opened" | [0x2b96…b272](https://explorer-studio.genlayer.com/tx/0x2b96c47343e1bf73135f3b1940599fa0375e294efde23b006c84b97f098ab272) |
| GV7 | `cast_vote(PROP0, "MAYBE")` as B. Reverts: "Support must be FOR or AGAINST" | [0xa95d…e645](https://explorer-studio.genlayer.com/tx/0xa95de279d07877a2e4fdc8795f3704925e833dc07b4ba1c6a5b206ac3a5ae645) |
| GV8 | `cast_vote(PROP0, "FOR")` as A (power 0). Reverts: "No voting power" | [0xeda7…756e](https://explorer-studio.genlayer.com/tx/0xeda70d5a05f21cf754fc21da70496bcb6768ee011f430a61772ea63e7935756e) |
| GV9 | `cast_vote(PROP0, "FOR")` as C (power 0). Reverts: "No voting power" | [0xae77…e8e6](https://explorer-studio.genlayer.com/tx/0xae776e77b97ef4cbff212625d714a605b105c4b6249c0a8524d4f49312fae8e6) |
| GV10 | `cast_vote(PROP0, "FOR")` as B (power 50). Success. for_weight 50, against_weight 0, voter_count 1 | [0x83a8…353b](https://explorer-studio.genlayer.com/tx/0x83a834f76b6ae385760ffe067aac7715b131888d5f4d1a9b550fd4c0336f353b) |
| GV11 | `cast_vote(PROP0, "AGAINST")` as B again. Reverts: "Already voted" | [0x3de4…c6a0](https://explorer-studio.genlayer.com/tx/0x3de471702cea6ebe3a624bda1ba39e97df0cdb780ec153a0a667a6b943dfc6a0) |
| GV12 | `close_voting(PROP0)` as B. Reverts: "Only the proposer can close voting" | [0xe0a4…326c](https://explorer-studio.genlayer.com/tx/0xe0a47c8156e952628eb975126bb042b651597d694cea8c8e9d5808093279326c) |
| GV13 | `close_voting(PROP0)` as A. Success, status CLOSED | [0xc3e4…dee8](https://explorer-studio.genlayer.com/tx/0xc3e49ae3c5f510e79120694e02a5fb00c7b8bd521a637735173cdbc5b5b4dee8) |
| GV14 | `cast_vote(PROP0, "FOR")` as C after close. Reverts: "Voting is not open" | [0x40b6…e9e4](https://explorer-studio.genlayer.com/tx/0x40b6f7647754364f8ba7e03392b4967b20e843fa1e2259cd5c15ade17ad6e9e4) |
| GV15 | Create PROP1 as A, open voting, then `close_voting(PROP1)` with zero votes. Last step reverts: "At least one vote is required to close" | [create](https://explorer-studio.genlayer.com/tx/0x75784761f26bd158dd5d5634aeceded9ec56ccb13192a04fb35306768a5804c8), [open](https://explorer-studio.genlayer.com/tx/0xbda87a72f3c0c3f4209b8b18d3effdff4f7fafbf6a73d11ac3958928f6672c8e), [close](https://explorer-studio.genlayer.com/tx/0x39fe5aae2a0242d7676e2cfca4c6ea8afdedc1c1a8b525be8afdebaed3ac037a) |
| PX1 | `execute_proposal(PROP0, 100)`. Reverts: "Quorum not met" | [0xb8b1…f804](https://explorer-studio.genlayer.com/tx/0xb8b1a9190ff32c290497fa8ce3bdce0ae08a2937cf004e0e858a1bd87c54f804) |
| PX2 | `execute_proposal(PROP0, 0)`. Reverts: "min_total_weight must be positive" | [0xf1e5…2403](https://explorer-studio.genlayer.com/tx/0xf1e5cfa2d7c3c17ca2934c0bc5c191fb455c39eaa7afab1a96c4cf9f5df62403) |
| PX3 | `execute_proposal(PROP0, 50)`. Success, returns "PASSED". for_weight 50, against_weight 0, min_total_weight 50 | [0x1dce…3dc9](https://explorer-studio.genlayer.com/tx/0x1dce014c507acf11f158bb4e78fdb40855bdb96fac185364bf5c946976f33dc9) |
| PX4 | `execute_proposal(PROP0, 50)` again. Reverts: "Proposal already executed" | [0xbb2f…7d4b](https://explorer-studio.genlayer.com/tx/0xbb2f3229d5b49698da2f7818283aba5b4d4d95cf03f6b4653aa745ff96157d4b) |
| PX5 | `execute_proposal(PROP1, 1)`, voting still open. Reverts: "Voting has not been closed yet" | [0x54ec…2ff5](https://explorer-studio.genlayer.com/tx/0x54ec42de3b5dc7473219e0087f2cbba0a36e45b13d128554b0af2987f79b2ff5) |
| PX6 | `execute_proposal(999, 1)`. Reverts: "Voting not found" | [0x5215…7f36](https://explorer-studio.genlayer.com/tx/0x5215626a24161734544c058824d678d6e1a3db131331a3ad63f65c4e5f3f7f36) |

### Cluster G: PredictionMarket + MarketOracleSettlement

Tests: 26

Internal points only, no real funds.

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| MK1 | `set_oracle(MarketOracleSettlement)` as B. Reverts: "Only deployer can set the oracle" | [0x9ac0…ea89](https://explorer-studio.genlayer.com/tx/0x9ac0c321577d8a1515530723498d2b29522d18744cbddd55c3cf1a80562fea89) |
| MK2 | `set_oracle(MarketOracleSettlement)` as A. Success | [0x6d96…c52f](https://explorer-studio.genlayer.com/tx/0x6d9612a9efbc1be8ac8353b6124e05886e7f7f2bb4b4e0ddabaf0d36cc9ac52f) |
| MK3 | `set_oracle(any)` as A again. Reverts: "Oracle already set" | [0xb5fd…ef1a](https://explorer-studio.genlayer.com/tx/0xb5fd607e9d003dd8d6a8a8bbed4e3f6c414382fb247a8ecfd30254d8fd5aef1a) |
| MK4 | `claim_points()` as A and as B. Both succeed, balance 100 each | [A](https://explorer-studio.genlayer.com/tx/0xe1021f17e6a87baac3a8e9fc70bde08296311ba8a1e94e78ef043de3b2f75d61), [B](https://explorer-studio.genlayer.com/tx/0x2d17be6d3332c99fc8e1a2e0ee37cb027bd1dea83a57846d16be487de760bb90) |
| MK5 | `claim_points()` as A again. Reverts: "Points already claimed" | [0x8eee…252f](https://explorer-studio.genlayer.com/tx/0x8eee23de5eb4d8153b00dc032df81a5fb3dce71d1a721a36081efaa197ae252f) |
| MK6 | `create_market("Is Python a programming language?", "not_a_url")`. Reverts: "Invalid source URL" | [0x50a0…b697](https://explorer-studio.genlayer.com/tx/0x50a0952e31d1b2cb1730c9bcc95ee1378d79f610c2c855736b5f37c8d9b4b697) |
| MK7 | `create_market(..., python.org/about)` as A. Success, M0 = 0 | [0xced7…aaff](https://explorer-studio.genlayer.com/tx/0xced74170852bc506f4a3e51a503487b07b26c208c6f6f7fcea7b766fd6e7aaff) |
| MK8 | `place_bet(M0, "YES", 30)` as A. Success, balance 70 | [0x8810…7f58](https://explorer-studio.genlayer.com/tx/0x88103f0f3fbd804acb0723cabcc43357c51422304dad37afc8852e64b6ef7f58) |
| MK9 | `place_bet(M0, "NO", 20)` as B. Success, balance 80 | [0xd5cb…4ce9](https://explorer-studio.genlayer.com/tx/0xd5cbd21c0279bfc819bf2806f786f8a08382e558f02e31ec00ab6d0c02794ce9) |
| MK10 | `place_bet(M0, "MAYBE", 5)` as A. Reverts: "Side must be YES or NO" | [0x24b3…afe1](https://explorer-studio.genlayer.com/tx/0x24b307377c455472cbd74730b602ce6c25c6d69d7f81b7e928d0d3124699afe1) |
| MK11 | `place_bet(M0, "YES", 0)` as A. Reverts: "Amount must be positive" | [0xc8a6…cb4a](https://explorer-studio.genlayer.com/tx/0xc8a6653e8ea6426bf7171cb4dd2bbb9f61a117246365c8bdec92d85c4f7dcb4a) |
| MK12 | `place_bet(M0, "YES", 1000)` as A. Reverts: "Insufficient points" | [0x65a1…45b8](https://explorer-studio.genlayer.com/tx/0x65a1d4aeddc25447a303ecd7af2471248e74f6a600c89455c377d6ef732245b8) |
| MK13 | `get_market_data(M0)`. yes_pool 30, no_pool 20, status OPEN, outcome empty | read-only call |
| MK14 | `close_market(M0)` as B. Reverts: "Only the creator can close the market" | [0xc8bc…f42c](https://explorer-studio.genlayer.com/tx/0xc8bc0a70262159d7de27d5b25a8a27540d41a3f815e4cfe2e5a76bacf667f42c) |
| MK15 | `settle_market(M0)` while OPEN. Reverts: "Market must be closed before settlement" | [0x8f6e…22b8](https://explorer-studio.genlayer.com/tx/0x8f6e8ffcfd8c0e0762a4eec6fa416d2f05a44c66cbaf439a3ae8b06da2bc22b8) |
| MK16 | `resolve_market(M0)` on MarketOracleSettlement while OPEN. Reverts: "Market must be closed before resolution" | [0xf0fb…497f](https://explorer-studio.genlayer.com/tx/0xf0fbe86c083c9a94f08f6fde84e2035c1f733a9f4c333fb55be22012815e497f) |
| MK17 | `close_market(M0)` as A. Success | [0x0273…f139](https://explorer-studio.genlayer.com/tx/0x0273bd35632bb571c0fb63aed21a9029efbef0d28d128543ccb0c37e5c63f139) |
| MK18 | `place_bet(M0, "YES", 5)` as A after close. Reverts: "Market is not open for bets" | [0x4f7c…a4e0](https://explorer-studio.genlayer.com/tx/0x4f7c2d12b13f179535d59396e74949609a9c88e552270c85b960c4746dc3a4e0) |
| MK19 | `settle_market(M0)` before resolution. Reverts: "No resolution found in oracle" | [0x67f1…a5c3](https://explorer-studio.genlayer.com/tx/0x67f16fd9da618d37d2d43614323a8b84d23e083fc0150ed15bd63d821cffa5c3) |
| MK20 | `resolve_market(M0)`. Success, answer "YES", source_fetched true, status RESOLVED | [0xed04…8536](https://explorer-studio.genlayer.com/tx/0xed04ca8ce461fed8661d68b9cd3b20b8fc2010b67ae72f0a3aceb0d92f218536) |
| MK21 | `resolve_market(M0)` again. Reverts: "Market already resolved" | [0xbe5b…3870](https://explorer-studio.genlayer.com/tx/0xbe5b2f95ab4812bd2ef486671d1266e020526ac1ec6fde734fe9e7ab19f23870) |
| MK22 | `settle_market(M0)`. Success, status SETTLED, outcome "YES", yes_pool 30, no_pool 20 | [0x240f…99e9](https://explorer-studio.genlayer.com/tx/0x240fc129b4b7894cd0dd152a008ef8af85b82fc777dca7d4bb6a7b89005299e9) |
| MK23 | `claim_winnings(M0)` as A returns 50, balance 120. As B reverts: "Nothing to claim", balance stays 80 | [A](https://explorer-studio.genlayer.com/tx/0xedbacc5e1adb25f3ae06441e0e75b807e549aaf967c55ac4b4f9bc67900e16f2), [B](https://explorer-studio.genlayer.com/tx/0xc1599c2eba0f7cdfdfb24b4d1a6ab1c771f56c9085a2c4804f3d20bf581735c5) |
| MK24 | `claim_winnings(M0)` as A again. Reverts: "Already claimed" | [0x34de…0745](https://explorer-studio.genlayer.com/tx/0x34de177cad07f16845fbafa0e3c5ae01f7c4d844741dc69264507c0b0d240745) |
| MK25 | `resolve_market(999)` on MarketOracleSettlement. Reverts: "Market not found" | [0x14bb…fc23](https://explorer-studio.genlayer.com/tx/0x14bbc967c6895b48d86c362002737d0a577a157556c6f7c03e15442edef4fc23) |
| MK26 | Create M1 as A, then `claim_winnings(M1)`. Last step reverts: "Market is not settled" | [create](https://explorer-studio.genlayer.com/tx/0x7b1335645cccadad736631fd2debf991ff7c1a25d2117a05422febeac3082f6c), [claim](https://explorer-studio.genlayer.com/tx/0x89219df6ad0095d0eb9d71362c9f3c7dd1000a62ab8aa431520fdd0aa8ceabd1) |

### Cluster H: ChallengeableAssertion + ChallengeOutcomeLedger

Tests: 23

CH14 has three steps (a, b, c) and counts as one test.

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| CH1 | `assert_claim("", wikipedia/Guido)`. Reverts: "Statement cannot be empty" | [0xe369…d213](https://explorer-studio.genlayer.com/tx/0xe369de038c2902ca21d1a2310f83421141e1cafff6747b9166eefc3c2d7ed213) |
| CH2 | `assert_claim("x", "not_a_url")`. Reverts: "Invalid evidence URL" | [0x9100…5385](https://explorer-studio.genlayer.com/tx/0x9100cdc275510f2971086881b1350f3bfc0ec89b6eb4f05af76ddd9b63795385) |
| CH3 | `assert_claim("Python was created by Guido van Rossum", wikipedia/Guido_van_Rossum)` as A. Success, AS0 = 0 | [0x29e4…2de8](https://explorer-studio.genlayer.com/tx/0x29e4a5b4d460e276ee9bb3528dabdef93733a20720292886071efe238ced2de8) |
| CH4 | `challenge(AS0, python.org/about)` as B while PENDING. Reverts: "Only an accepted assertion can be challenged" | [0x3433…a91e](https://explorer-studio.genlayer.com/tx/0x3433ba2acfc3c71083cef27d45fcc030936f0e42ca74b8fffedb7da13edea91e) |
| CH5 | `evaluate(AS0)` as A. Success, label "SUPPORTED", status ACCEPTED | [0x70f7…9d23](https://explorer-studio.genlayer.com/tx/0x70f7663354851948c3ca6cce3357e7cf453aa8eb5dd780c09124fff00ebb9d23) |
| CH6 | `evaluate(AS0)` again. Reverts: "Assertion already evaluated" | [0x75fa…f0af](https://explorer-studio.genlayer.com/tx/0x75fa482dfd831d169222880882aa39592a7e967647bc86b6c36059f77223f0af) |
| CH7 | `challenge(AS0, python.org/about)` as A. Reverts: "Asserter cannot challenge their own assertion" | [0x6af3…90f7](https://explorer-studio.genlayer.com/tx/0x6af362b648a5df1d2cf29fcda098844209393f700c8a295050e51e74b46790f7) |
| CH8 | `challenge(AS0, wikipedia/Guido_van_Rossum)` as B, same as original. Reverts: "Counter-evidence must differ from the original evidence" | [0x582d…4a7f](https://explorer-studio.genlayer.com/tx/0x582dba67ea0b7f1ce08998162b9756be88df40279e3fd919734900b5cbdd4a7f) |
| CH9 | `challenge(AS0, "not_a_url")` as B. Reverts: "Invalid counter URL" | [0x9dbd…11a2](https://explorer-studio.genlayer.com/tx/0x9dbd9f788472587fd43fd898f8cf73a4325a38871bc197c7d37ed1e5840811a2) |
| CH10 | `resolve_challenge(AS0)` while ACCEPTED. Reverts: "Assertion is not under challenge" | [0x5d3b…4488](https://explorer-studio.genlayer.com/tx/0x5d3ba3a86832ae81248027cc20c665f0ce86aa79c6302677c001628c138f4488) |
| CH11 | `challenge(AS0, python.org/about)` as B. Success, status CHALLENGED | [0x4dd5…8d40](https://explorer-studio.genlayer.com/tx/0x4dd5d7045fb0589dcfeb56ba1adee1ae991a1fbadd6906c0f03cd90635388d40) |
| CH12 | `challenge(AS0, python.org/downloads)` as B while CHALLENGED. Reverts: "Only an accepted assertion can be challenged" | [0xe38a…7b62](https://explorer-studio.genlayer.com/tx/0xe38a6470a2507827d641fa911ff3f870f2338bf02ede6c22bc6a47b567807b62) |
| CH13 | `resolve_challenge(AS0)`. Success, label "SUPPORTED", status ACCEPTED, stage 2 | [0x4deb…4091](https://explorer-studio.genlayer.com/tx/0x4debb74038e5ab372f8af81fe59661ff2bf64460c785977d93a9edfd68f24091) |
| CH14.a | `challenge(AS0, python.org/about)` as B, same counter-evidence as the previous challenge. Reverts: "Counter-evidence must differ from the previous counter-evidence" | [0x2a73…1385](https://explorer-studio.genlayer.com/tx/0x2a73cc0425c3c8eccce68f397fa39a2122424a3cb5423a4f3b58f05492b41385) |
| CH14.b | `challenge(AS0, python.org/downloads)` as B. Success | [0x35ce…0781](https://explorer-studio.genlayer.com/tx/0x35cebb9e78e605db8ab7ec3c5ebabe385da1d74ced451bf2c9516bbcc0660781) |
| CH14.c | `resolve_challenge(AS0)`. Success, label "SUPPORTED", status FINALIZED_ACCEPTED, stage 3 | [0x584b…ca10](https://explorer-studio.genlayer.com/tx/0x584be4bfe896665ae11e5445397aa710a2129ef7448936c20d8e6950124fca10) |
| CH15 | `challenge(AS0, python.org)` as B on a FINALIZED assertion. Reverts: "Only an accepted assertion can be challenged" | [0x37d9…1a5f](https://explorer-studio.genlayer.com/tx/0x37d9e0c21d3b54d1c2045b2075f0b764e7d53b75acb36b5f9ffdfb689f891a5f) |
| CH16 | `assert_claim("The Moon is made of cheese", wikipedia/Moon)` as A (AS1 = 1), then `evaluate(AS1)`. Label "UNSUPPORTED", status REJECTED | [assert](https://explorer-studio.genlayer.com/tx/0x22897e44d286d39af6a362783efc1e3355d269cf37a762633f37b7310c5bc72f), [evaluate](https://explorer-studio.genlayer.com/tx/0xb004391b477953cc3811b3c0fdf60c1225d7095a9dea4774cb2509473085715c) |
| CH17 | `assert_claim("Another claim", python.org/about)` as A. Success, AS2 = 2 (left PENDING) | [0x7488…40a6](https://explorer-studio.genlayer.com/tx/0x7488c1dad587dee7beb183979f95e4228fcb57fe1dce5542e678f5ec31ab40a6) |
| OL1 | `record_outcome(AS1)` as A. final_status "REJECTED", stages 1, upheld false. Agent record: upheld 0, lost 1 | [0x5f96…94aa](https://explorer-studio.genlayer.com/tx/0x5f96ca1720735b2a1b34cbb2e61d9618c9cfaeaf1191e3add41808e6911894aa) |
| OL2 | `record_outcome(AS0)` as A. Agent record: upheld 1, lost 1 (sum 2 matches 2 recorded assertions) | [0x20aa…2ed8](https://explorer-studio.genlayer.com/tx/0x20aa98d9aae2d53564d8775c8623b7df43aae9a8e3de7409f61e98f8a4d12ed8) |
| OL3 | `record_outcome(AS0)` again. Reverts: "Outcome already recorded" | [0x07b8…af54](https://explorer-studio.genlayer.com/tx/0x07b871578febceddac17b6ea71e9403f1fd3bc8ea9fb7ecfd591bc15467faf54) |
| OL4 | `record_outcome(AS2)`, still PENDING. Reverts: "Assertion has not reached a final status" | [0x6c68…6a09](https://explorer-studio.genlayer.com/tx/0x6c68893ed30e6ac02b3884f3cd909f781fc58ab0e80a3ac29a003243f1616a09) |
| OL5 | `record_outcome(999)`. Reverts: "Assertion not found" | [0x27ec…bc26](https://explorer-studio.genlayer.com/tx/0x27ecb1871c3b6e9646d757fb933d0f6a91055feb850cd3cfa9e85c70639dbc26) |
| OL6 | `list_outcomes()` = "0:FINALIZED_ACCEPTED,1:REJECTED" | read-only call |

### Cluster PT: Post-test service liveness recovery

Tests: 2

| Test Code | Description | Tx Link |
|-----------|-------------|---------|
| PT1 | `heartbeat()` as C in the next epoch. Success. C recovers from DOWN to ACTIVE: consecutive_missed 0, total_beats 2, total_missed 2, epochs_observed 4 | [0x7a35…60a9](https://explorer-studio.genlayer.com/tx/0x7a35f6346ef046567bfd2a4868efdf63802ace7955b4ee0311fa36d8c14460a9) |
| PT2 | `apply_liveness(C)`. Success, change_id 2. uptime = 2*100//4 = 50, above 33+10, so INCREASE. `get_reputation(C)` = "REPUTATION:50" | [0x19fc…442b](https://explorer-studio.genlayer.com/tx/0x19fccaf3a525b0518c7e52702e65093808159c3a44d3e69df229c1a664f0442b) |

---

## Section 4: Summary

- Total Contracts: 17
- Total Tests: 171
- Total Passed: 171
- Total Failed: 0

| Cluster | Contracts | Tests |
|---------|-----------|-------|
| B | CommitRevealVote, CommitRevealResolver | 24 |
| A | AmbiguityOracle | 14 |
| DS | DissensusScorer | 9 |
| C | SemanticAccessGate, AccessAuditLog | 20 |
| D | ProofRegistry, StructuredProofChecker | 10 |
| E | ServiceHeartbeatMonitor, LivenessReputationLink | 22 |
| F | ProposalRegistry, WeightedVoting, ProposalExecutor | 21 |
| G | PredictionMarket, MarketOracleSettlement | 26 |
| H | ChallengeableAssertion, ChallengeOutcomeLedger | 23 |
| PT | ServiceHeartbeatMonitor, LivenessReputationLink | 2 |
| **Total** | **17 contracts** | **171** |

Tests that expect a revert count as passed when the contract reverts with the expected error.

---

## Section 5: Empirical Results Summary

These tests have outputs decided by the LLM validators inside the contracts, so the exact result is not fixed in advance. Every result below fell inside the documented set of valid outcomes, and none was treated as a failure.

| Test Code | Call | Result |
|-----------|------|--------|
| AM9 | `judge_question(Q0)` | TRUE |
| AM10 | `judge_question(Q1)` | AMBIGUOUS |
| AM11 | `judge_question(Q2)` | AMBIGUOUS |
| AM12 | `judge_question(Q3)` | TRUE |
| DS4 | `score_panel("0,1,2")` | true=1, false=0, ambiguous=2, majority=AMBIGUOUS, dissensus=34 |
| SG8 | `decide_access(REQ0)` | GRANTED |
| SG9 | `decide_access(REQ1)` | DENIED |
| PC1 | `check_proof(P0)` | INCOMPLETE |
| PC2 | `check_proof(P1)` | INVALID |
| MK20 | `resolve_market(M0)` | YES (source_fetched=true) |
| CH5 | `evaluate(AS0)` | SUPPORTED, status ACCEPTED |
| CH13 | `resolve_challenge(AS0)` | SUPPORTED, status ACCEPTED, stage 2 |
| CH14 | `resolve_challenge(AS0)` | SUPPORTED, status FINALIZED_ACCEPTED, stage 3 |
| CH16 | `evaluate(AS1)` | UNSUPPORTED, status REJECTED |

---

## Section 6: Key Math Verifications

**1. DS4 dissensus score**

- Panel: 1 TRUE, 0 FALSE, 2 AMBIGUOUS
- majority = AMBIGUOUS (2 of 3)
- dissensus_score = 34

**2. LR2 uptime (B)**

- beats = 3, missed = 0, epochs = 3
- uptime = 3\*100//3 = 100, so INCREASE
- reputation(B) = 100

**3. LR4 uptime (C)**

- beats = 1, missed = 2, epochs = 3
- uptime = 1\*100//3 = 33, so DECREASE
- reputation(C) = 33

**4. MK23 pool math**

- yes_pool = 30, no_pool = 20, outcome = YES, total = 50
- A claim = (30 \* 50) // 30 = 50
- balance(A) = 70 + 50 = 120
- balance(B) = 80 (unchanged)

**5. PT2 uptime (C)**

- beats = 2, missed = 2, epochs = 4
- uptime = 2\*100//4 = 50
- previous reputation 33, and 50 > 33 + 10, so INCREASE
- reputation(C) = 50

**6. OL2 agent record sum**

- AS1 (REJECTED): lost = 1
- AS0 (FINALIZED_ACCEPTED): upheld = 1
- total = 2, matching the 2 recorded assertions

---

## Section 7: Security Model Verification

| Lesson from previous projects | Verified by test in this suite |
|-------------------------------|--------------------------------|
| Agent bound to real sender | Registry: SG1, CH3; all writes |
| No caller-supplied JSON accepted | All downstream contracts: on-chain reads |
| Validator independently recomputes | AM, DS, SG, PC, MK, CH evaluate |
| No timestamp dependency | All contracts: manual epochs |
| No payable / no value transfer | Entire suite: no native value |
| Lazy default for reputation | LR5 = 50, PT2.b increased |
| Double-apply guards | Every stateful contract |
| URL validation | AM1, SG4, PR2, MK6, CH2, CH9 |
| Domain uniqueness | Not used here: single-URL checks |
| Optional final-status checks | DS7, OL4 (pending rejected) |
| Access grant single-shot | SG13 |
| Vote power = reputation above 50 | GV8, GV9 (rejected), GV10 |
| Challenge authorship guard | CH7 |
| Counter-evidence diff guard | CH8, CH14.a |
| Challenge-once-after-final guard | CH12, CH15 |
| Multi-stage challenge (up to 3) | CH5 → CH11 → CH13 → CH14.c |
| Resolution before settlement | MK16, MK19 |
| Outcome recording idempotency | OL3 |
| Final-status-only outcome recording | OL4 |
