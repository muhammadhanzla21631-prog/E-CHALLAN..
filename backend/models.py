from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Camera(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lat: float
    lng: float
    address: Optional[str] = None
    light_status: Optional[str] = "red" # red, yellow, green
    status: Optional[str] = "active" # active, inactive
    speed_limit: Optional[int] = 60 # km/h
    last_maintenance: Optional[str] = None
    total_violations: Optional[int] = 0
    health_score: Optional[int] = 100  # 0-100

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    cnic: Optional[str] = None  # National ID
    role: str = "user"  # user, admin
    created_at: Optional[str] = None
    last_login: Optional[str] = None

class UserToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fcm_token: str
    user_id: Optional[int] = None

class Challan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle: str
    camera_id: int
    amount: float
    violation_type: Optional[str] = "traffic_violation"  # overspeed, red_light, no_helmet, etc.
    status: str = "unpaid"  # unpaid, paid, appealed, dismissed
    user_id: Optional[int] = None
    issued_at: Optional[str] = None
    paid_at: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    challan_id: int = Field(foreign_key="challan.id")
    user_id: Optional[int] = None
    amount: float
    payment_method: str  # card, bank_transfer, easypay, jazzcash
    transaction_id: Optional[str] = None
    status: str = "pending"  # pending, completed, failed
    created_at: Optional[str] = None
    completed_at: Optional[str] = None

class Appeal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    challan_id: int = Field(foreign_key="challan.id")
    user_id: int = Field(foreign_key="user.id")
    reason: str
    status: str = "pending"  # pending, approved, rejected
    created_at: Optional[str] = None
    reviewed_at: Optional[str] = None
    reviewer_notes: Optional[str] = None
