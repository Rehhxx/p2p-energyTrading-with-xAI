from app.model.trade import TradeRequest, TradeResponse
from datetime import datetime, timezone
import hashlib
import logging

logging.basicConfig(level=logging.INFO)

class TradeService:
    def __init__(self):
        # Simulated user energy balances(will change in future)
        self.user_energy = {
            "user123": 10000.0,
            "user456": 5000.0,
            "user789": 7500.0
        }

        self.registered_users = set(self.user_energy.keys())
        self.trade_history = []

    def process_trade(self, trade: TradeRequest) -> TradeResponse:
        self._log_trade_attempt(trade)
        self._validate_user(trade)
        self._validate_trade(trade)
        self._check_balances(trade)

        self._deduct_energy(trade.seller_id, trade.energy_amount)
        trade_hash = self._generate_trade_hash(trade)
        self._log_trade_success(trade, trade_hash)
        self.trade_history.append({
            "trade": trade,
            "hash": trade_hash,
            "timestamp": datetime.utcnow()
        })

        return TradeResponse(
            seller_id=trade.seller_id,
            buyer_id=trade.buyer_id,
            energy_amount=trade.energy_amount,
            price_per_unit=trade.price_per_unit,
            total_price=trade.energy_amount * trade.price_per_unit,
            status="completed",
            timestamp=trade.timestamp,
            message="Trade processed successfully",
            trade_hash=trade_hash
        )
    
    def _log_trade_attempt(self, trade: TradeRequest):
        logging.info(f"Attempting trade: {trade.buyer_id} buys {trade.energy_amount} units from {trade.seller_id}")
    
    def _log_trade_success(self, trade: TradeRequest, trade_hash: str):
        logging.info(f"Trade successful: {trade.buyer_id} <- {trade.energy_amount} units | Hash: {trade_hash}")

    def _validate_user(self, trade: TradeRequest):
        for user in [trade.buyer_id, trade.seller_id]:
            if user not in self.registered_users:
                logging.error(f"User {user} is not registered.")
                raise ValueError(f"User {user} is not registered.")
    
    #Internal validation methods
    def _validate_trade(self, trade: TradeRequest):
        if trade.energy_amount <= 0:
            raise ValueError("Energy amount must be greater than zero.")
        if trade.price_per_unit <= 0:
            raise ValueError("Price per unit must be greater than zero.")
        if trade.buyer_id == trade.seller_id:
            raise ValueError("Buyer and seller cannot be the same entity.")
        now_utc = datetime.now(timezone.utc)
        trade_time = trade.timestamp
        if trade_time.tzinfo is None:
            trade_time = trade_time.replace(tzinfo=timezone.utc)
        if trade_time > now_utc:
            raise ValueError("Trade timestamp cannot be in the future.")
        
    def _check_balances(self, trade: TradeRequest):
        if self.user_energy[trade.seller_id] < trade.energy_amount:
            raise ValueError(f"Seller '{trade.seller_id}' does not have enough energy to sell.")
        
    def _deduct_energy(self, seller_id: str, amount: float):
        self.user_energy[seller_id] -= amount

    def _generate_trade_hash(self, trade: TradeRequest) -> str:
        data = f"{trade.buyer_id}:{trade.seller_id}:{trade.energy_amount}:{trade.price_per_unit}:{trade.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    #Get trade history, user balance and all balances
    def get_trade_history(self):
        return self.trade_history

    def get_user_balance(self, user_id: str) -> float:
        return self.user_energy.get(user_id, 0.0)
    
    def get_all_balances(self):
        return self.user_energy