"""Database models using SQLAlchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum as python_enum

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    subscriptions = relationship("Subscription", back_populates="user")
    strategies = relationship("Strategy", back_populates="user")
    orders = relationship("Order", back_populates="user")


class PlanType(python_enum.Enum):
    """Subscription plan types"""
    FREE = "FREE"
    BASIC = "BASIC"
    PRO = "PRO"


class Subscription(Base):
    """User subscription plan"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan = Column(Enum(PlanType), default=PlanType.FREE)
    stripe_subscription_id = Column(String(255))
    starts_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="subscriptions")


class Strategy(Base):
    """Trading strategy"""
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255))
    description = Column(Text)
    rule_json = Column(Text)  # JSON rules
    is_active = Column(Boolean, default=False)
    paper_trading = Column(Boolean, default=True)
    max_daily_loss = Column(Float, default=5000.0)
    max_trades_per_day = Column(Integer, default=50)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="strategies")
    orders = relationship("Order", back_populates="strategy")


class OrderStatus(python_enum.Enum):
    """Order states"""
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    SENT = "SENT"
    ACK = "ACK"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"


class Order(Base):
    """Order record"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    symbol = Column(String(20), index=True)
    order_type = Column(String(20))  # MARKET, LIMIT
    side = Column(String(10))  # BUY, SELL
    quantity = Column(Float)
    price = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED)
    client_order_id = Column(String(255), unique=True)
    broker_order_id = Column(String(255))
    filled_quantity = Column(Float, default=0.0)
    avg_price = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
    paper_trading = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="orders")
    strategy = relationship("Strategy", back_populates="orders")


class Position(Base):
    """Open position"""
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    symbol = Column(String(20), index=True)
    quantity = Column(Float)
    entry_price = Column(Float)
    current_price = Column(Float)
    pnl = Column(Float)
    pnl_percent = Column(Float)
    paper_trading = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    """Audit log for compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255))
    details = Column(Text)
    ip_address = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
