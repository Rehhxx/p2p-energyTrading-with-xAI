from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from app.services.trade_services import TradeService

router = APIRouter()
trade_service = TradeService()

# Request Models
class TradeRequest(BaseModel):
    seller_id: str
    buyer_id: str
    energy_amount: float
    price_per_unit: float


class UserBalanceRequest(BaseModel):
    user_id: str

# Routes
@router.post("/trade")
def execute_trade(trade: TradeRequest):
    """
    Execute a trade between seller and buyer for a specified amount of energy and price.
    """
    try:
        result = trade_service.process_trade(
            seller_id=trade.seller_id,
            buyer_id=trade.buyer_id,
            energy_amount=trade.energy_amount,
            price_per_unit=trade.price_per_unit
        )
        return {"status": "success", "message": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/balance/{user_id}")
def get_user_balance(user_id: str):
    """
    Get the energy balance of a user.
    """
    try:
        balance = trade_service.get_user_balance(user_id)
        return {"user_id": user_id, "energy_balance": balance}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/all-balances")
def get_all_balances():
    """
    Get energy balances for all users (for simulation/debugging purposes).
    """
    return trade_service.get_all_balances()
