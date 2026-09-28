# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import re

from genlayer import *
from dataclasses import dataclass

FAUCET_AMOUNT = 100


def clean_url(url: str):
    if not url:
        return None
    cleaned = url.strip().rstrip('/')
    if cleaned.startswith('http://'):
        cleaned = cleaned.replace('http://', 'https://', 1)
    cleaned = cleaned.replace(' ', '')
    if '?' in cleaned:
        cleaned = cleaned.split('?')[0]
    return cleaned if cleaned else None


def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r'^(https?://)'
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
        r'(/[\w\-./?%&=]*)?$'
    )
    return bool(pattern.match(url.strip()))


@allow_storage
@dataclass
class Market:
    market_id: u256
    creator: str
    question: str
    source_url: str
    status: str  # OPEN, CLOSED, SETTLED
    yes_pool: u256
    no_pool: u256
    outcome: str  # "", YES, NO, UNRESOLVED


class PredictionMarket(gl.Contract):
    # NOTE: this market runs on internal play-money "points", not native GEN,
    # so it never holds or transfers real funds.
    markets: TreeMap[u256, Market]
    balances: TreeMap[str, u256]
    faucet_claimed: TreeMap[str, u256]
    stakes: TreeMap[str, u256]
    claimed: TreeMap[str, u256]
    next_id: u256
    deployer: str
    oracle_contract: str
    oracle_set: bool

    def __init__(self):
        self.next_id = u256(0)
        self.deployer = str(gl.message.sender_address)
        self.oracle_contract = ""
        self.oracle_set = False

    @gl.public.write
    def set_oracle(self, oracle_address: str):
        # One-time, deployer-only. Resolves the circular deploy dependency
        # (the oracle reads this contract, and this contract reads the oracle).
        assert str(gl.message.sender_address) == self.deployer, "Only deployer can set the oracle"
        assert not self.oracle_set, "Oracle already set"
        assert oracle_address.strip() != "", "Oracle address cannot be empty"
        self.oracle_contract = oracle_address
        self.oracle_set = True

    @gl.public.write
    def claim_points(self):
        agent = str(gl.message.sender_address)
        assert agent not in self.faucet_claimed, "Points already claimed"
        self.faucet_claimed[agent] = u256(1)
        self.balances[agent] = self.balances.get(agent, u256(0)) + u256(FAUCET_AMOUNT)

    @gl.public.write
    def create_market(self, question: str, source_url: str) -> u256:
        assert question.strip() != "", "Question cannot be empty"
        cleaned = clean_url(source_url)
        assert cleaned is not None, f"Invalid source URL: {source_url}"
        assert is_valid_url(cleaned), f"Invalid source URL: {cleaned}"

        mid = self.next_id
        self.next_id += u256(1)
        self.markets[mid] = Market(
            market_id=mid,
            creator=str(gl.message.sender_address),
            question=question,
            source_url=cleaned,
            status="OPEN",
            yes_pool=u256(0),
            no_pool=u256(0),
            outcome="",
        )
        return mid

    @gl.public.write
    def place_bet(self, market_id: u256, side: str, amount: u256):
        assert market_id in self.markets, "Market not found"
        market = self.markets[market_id]
        assert market.status == "OPEN", "Market is not open for bets"

        side = side.strip().upper()
        assert side in ("YES", "NO"), "Side must be YES or NO"
        assert amount > u256(0), "Amount must be positive"

        agent = str(gl.message.sender_address)
        balance = self.balances.get(agent, u256(0))
        assert balance >= amount, "Insufficient points"

        self.balances[agent] = balance - amount
        stake_key = f"{int(market_id)}:{agent}:{side}"
        self.stakes[stake_key] = self.stakes.get(stake_key, u256(0)) + amount

        if side == "YES":
            market.yes_pool = market.yes_pool + amount
        else:
            market.no_pool = market.no_pool + amount
        self.markets[market_id] = market

    @gl.public.write
    def close_market(self, market_id: u256):
        assert market_id in self.markets, "Market not found"
        market = self.markets[market_id]
        assert str(gl.message.sender_address) == market.creator, "Only the creator can close the market"
        assert market.status == "OPEN", "Market is not open"
        market.status = "CLOSED"
        self.markets[market_id] = market

    @gl.public.write
    def settle_market(self, market_id: u256):
        assert self.oracle_set, "Oracle not set"
        assert market_id in self.markets, "Market not found"
        market = self.markets[market_id]
        assert market.status == "CLOSED", "Market must be closed before settlement"

        raw = gl.get_contract_at(
            Address(self.oracle_contract)
        ).view().get_resolution_data(market_id)
        assert raw != "NOT_FOUND", "No resolution found in oracle"

        try:
            data = json.loads(raw)
        except:
            raise gl.vm.UserError("Invalid data from oracle")

        outcome = data.get("outcome", "")
        assert outcome in ("YES", "NO", "UNRESOLVED"), "Invalid outcome from oracle"

        market.outcome = outcome
        market.status = "SETTLED"
        self.markets[market_id] = market

    @gl.public.write
    def claim_winnings(self, market_id: u256) -> u256:
        assert market_id in self.markets, "Market not found"
        market = self.markets[market_id]
        assert market.status == "SETTLED", "Market is not settled"

        agent = str(gl.message.sender_address)
        claim_key = f"{int(market_id)}:{agent}"
        assert claim_key not in self.claimed, "Already claimed"

        yes_stake = int(self.stakes.get(f"{int(market_id)}:{agent}:YES", u256(0)))
        no_stake = int(self.stakes.get(f"{int(market_id)}:{agent}:NO", u256(0)))
        yes_pool = int(market.yes_pool)
        no_pool = int(market.no_pool)
        total_pool = yes_pool + no_pool

        if market.outcome == "YES":
            winning_pool = yes_pool
            user_win = yes_stake
        elif market.outcome == "NO":
            winning_pool = no_pool
            user_win = no_stake
        else:
            winning_pool = 0
            user_win = 0

        if market.outcome not in ("YES", "NO") or winning_pool == 0:
            payout = yes_stake + no_stake  # refund
        else:
            payout = (user_win * total_pool) // winning_pool

        assert payout > 0, "Nothing to claim"

        self.balances[agent] = self.balances.get(agent, u256(0)) + u256(payout)
        self.claimed[claim_key] = u256(1)
        return u256(payout)

    @gl.public.view
    def get_balance(self, agent: str) -> str:
        return f"BALANCE:{int(self.balances.get(agent, u256(0)))}"

    @gl.public.view
    def get_stake(self, market_id: u256, agent: str, side: str) -> str:
        key = f"{int(market_id)}:{agent}:{side.strip().upper()}"
        return str(int(self.stakes.get(key, u256(0))))

    @gl.public.view
    def get_market_data(self, market_id: u256) -> str:
        if market_id not in self.markets:
            return "NOT_FOUND"
        m = self.markets[market_id]
        return json.dumps({
            "market_id": int(m.market_id),
            "creator": m.creator,
            "question": m.question,
            "source_url": m.source_url,
            "status": m.status,
            "yes_pool": int(m.yes_pool),
            "no_pool": int(m.no_pool),
            "outcome": m.outcome,
        })

    @gl.public.view
    def list_markets(self) -> str:
        items = []
        for key in self.markets:
            m = self.markets[key]
            items.append(f"{int(m.market_id)}:{m.status}")
        return ",".join(items)
