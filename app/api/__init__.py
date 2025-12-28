"""Comprehensive API endpoints for algo trading platform"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.database import get_db
from app.models import User, Strategy, Order
import logging

logger = logging.getLogger(__name__)

# Routers
users_router = APIRouter(prefix="/api/users", tags=["users"])
strategies_router = APIRouter(prefix="/api/strategies", tags=["strategies"])
orders_router = APIRouter(prefix="/api/orders", tags=["orders"])


# ============= SCHEMAS =============

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class StrategyCreate(BaseModel):
    name: str
    description: str
    rule_json: str
    max_daily_loss: float = 5000.0
    max_trades_per_day: int = 50


class StrategyResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    paper_trading: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    symbol: str
    order_type: str
    side: str
    quantity: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= USER ENDPOINTS =============

@users_router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register new user"""
    # Check if user exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    # Create user
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user = User(
        email=user_data.email,
        hashed_password=pwd_context.hash(user_data.password),
        full_name=user_data.full_name,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"User registered: {user.email}")
    return user


@users_router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int,  # In production, get from JWT
    db: Session = Depends(get_db)
):
    """Get current user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ============= STRATEGY ENDPOINTS =============

@strategies_router.post("/", response_model=StrategyResponse)
async def create_strategy(
    strategy_data: StrategyCreate,
    user_id: int,  # From JWT in production
    db: Session = Depends(get_db)
):
    """Create new strategy"""
    
    # Validate rule JSON
    from app.engine.rules import RuleEngine
    engine = RuleEngine()
    if not engine.register_rule(0, strategy_data.rule_json):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid rule JSON"
        )
    
    strategy = Strategy(
        user_id=user_id,
        name=strategy_data.name,
        description=strategy_data.description,
        rule_json=strategy_data.rule_json,
        max_daily_loss=strategy_data.max_daily_loss,
        max_trades_per_day=strategy_data.max_trades_per_day,
        paper_trading=True,  # Always start with paper
    )
    
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    
    logger.info(f"Strategy created: {strategy.name} by user {user_id}")
    return strategy


@strategies_router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(
    strategy_id: int,
    user_id: int,  # From JWT
    db: Session = Depends(get_db)
):
    """Get strategy (scoped by user)"""
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == user_id
    ).first()
    
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    return strategy


@strategies_router.post("/{strategy_id}/toggle")
async def toggle_strategy(
    strategy_id: int,
    user_id: int,  # From JWT
    db: Session = Depends(get_db)
):
    """Toggle strategy active/inactive"""
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == user_id
    ).first()
    
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    strategy.is_active = not strategy.is_active
    db.commit()
    
    logger.info(f"Strategy {strategy_id} toggled: {strategy.is_active}")
    return {
        "id": strategy.id,
        "name": strategy.name,
        "is_active": strategy.is_active,
    }


# ============= ORDER ENDPOINTS =============

@orders_router.get("/", response_model=list[OrderResponse])
async def get_user_orders(
    user_id: int,  # From JWT
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get user's orders"""
    orders = db.query(Order).filter(
        Order.user_id == user_id
    ).order_by(Order.created_at.desc()).limit(limit).all()
    
    return orders


@orders_router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    user_id: int,  # From JWT
    db: Session = Depends(get_db)
):
    """Get specific order"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


# ============= KILL SWITCH ENDPOINT =============

@orders_router.post("/kill-switch")
async def activate_kill_switch(
    user_id: int,  # From JWT
    db: Session = Depends(get_db)
):
    """Activate kill switch - cancel all active orders"""
    
    # Get all active orders for user
    active_orders = db.query(Order).filter(
        Order.user_id == user_id,
        Order.status.in_(["CREATED", "VALIDATED", "SENT", "ACK", "PARTIAL"])
    ).all()
    
    cancelled = 0
    for order in active_orders:
        order.status = "CANCELED"
        cancelled += 1
    
    db.commit()
    
    logger.critical(f"KILL SWITCH ACTIVATED for user {user_id}. Cancelled {cancelled} orders.")
    
    return {
        "status": "kill_switch_activated",
        "orders_cancelled": cancelled,
        "timestamp": datetime.utcnow().isoformat(),
    }
