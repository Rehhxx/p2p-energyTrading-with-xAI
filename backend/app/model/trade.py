from pydantic import BaseModel, Field, validator
from typing import Literal
from datetime import datetime
import uuid

class TradeRequest(BaseModel):
    seller_id: str = Field(..., min_length = 3, max_length = 50, example = "user_seller_001")
    buyer_id: str = Field(..., min_length = 3, max_length = 50, example = "user_buyer_007")
    energy_amount: float = Field(..., gt = 0, le = 10000, example = 50.0)
    price_per_unit: float = Field(..., gt = 0, le = 1000, example = 5.5)

    @validator("seller_id", "buyer_id")
    def validate_ids(cls, v):
        if v.strip() == "":
            raise ValueError("ID cannot be empty")
        return v
    
    @validator("buyer_id")
    def buyer_and_seller_differ(cls, v, values):
        if "seller_id" in values and values["seller_id"] == v:
            raise ValueError("Buyer and seller cannot be the same")
        return v
    
class TradeResponse(BaseModel):
    trade_id: str = Field(default_factory = lambda: str(uuid.uuid4()))
    seller_id: str
    buyer_id: str
    energy_amount: float
    price_per_unit: float
    total_price: float = Field(..., description="Computed total cost of the trade (energy_amount * price_per_unit)")
    status: Literal["pending", "completed", "failed"] = "pending"
    timestamp: datetime = Field(default_factory = datetime.utcnow)
    message: str = Field(default="")
    trade_hash: str = Field(default="")

    @classmethod
    def from_request(cls, request: TradeRequest, status: str = "pending"):
        return cls(
            seller_id = request.seller_id,
            buyer_id = request.buyer_id,
            energy_amount = request.energy_amount,
            price_per_unit = request.price_per_unit,
            total_price = request.energy_amount * request.price_per_unit,
            status = status
        )
                        
        

