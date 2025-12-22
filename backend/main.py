from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List, Optional
from sqlmodel import select
from utils.predictors import predict_image, get_device_info
from utils.notifications import send_email_notification, send_whatsapp_notification
from db import init_db, get_session
from models import Camera, UserToken, Challan, User, Payment, Appeal
from fcm import send_push


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
def on_startup():
    init_db()


# Simple load of camera data from file (for demo)
@app.get('/api/cameras', response_model=List[Camera])
def get_cameras():
    with get_session() as s:
        cams = s.exec(select(Camera)).all()
        return cams


@app.post('/api/register-fcm')
def register_fcm(token: UserToken):
    with get_session() as s:
        s.add(token)
        s.commit()
        s.refresh(token)
        return {"ok": True, "id": token.id}


@app.post('/api/challan')
def issue_challan(vehicle: str, camera_id: int, amount: float, user_id: Optional[int] = None):
    with get_session() as s:
        challan = Challan(vehicle=vehicle, camera_id=camera_id, amount=amount, user_id=user_id)
        s.add(challan)
        s.commit()
        s.refresh(challan)
        
        # Notification Logic
        message_body = f"Challan Issued! Vehicle: {vehicle}, Amount: {amount}, ID: {challan.id}"
        
        # 1. FCM Push
        tokens = s.exec(select(UserToken)).all()
        for t in tokens:
            try:
                send_push(t.fcm_token, "New Challan Issued", f"Vehicle {vehicle} fined {amount}", {"type":"challan","id":str(challan.id)})
            except Exception as e:
                print('FCM error', e)
                
        # 2. Email & WhatsApp (if user known)
        if user_id:
            user = s.get(User, user_id)
            if user:
                # Email
                if user.email:
                    send_email_notification(user.email, "E-Challan Notification", message_body)
                # WhatsApp
                if user.phone:
                    send_whatsapp_notification(user.phone, message_body)

        return {"ok": True, "challan_id": challan.id}


# simple endpoint to add camera (admin)
@app.post('/api/camera')
def add_camera(camera: Camera):
    with get_session() as s:
        s.add(camera)
        s.commit()
        s.refresh(camera)
        return camera


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = predict_image(image_bytes)
    return {"prediction": result}

# User Authentication Endpoints
from datetime import datetime
import hashlib

@app.post('/api/register')
def register_user(username: str, email: str, password: str, full_name: str = None):
    with get_session() as s:
        # Check if user exists
        existing = s.exec(select(User).where(User.username == username)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Hash password (simple demo - use proper hashing in production)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            created_at=datetime.now().isoformat()
        )
        s.add(user)
        s.commit()
        s.refresh(user)
        return {"success": True, "user_id": user.id, "username": user.username}

@app.post('/api/login')
def login_user(username: str, password: str):
    with get_session() as s:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = s.exec(select(User).where(
            User.username == username,
            User.password_hash == password_hash
        )).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role
            }
        }

# Analytics Endpoints
@app.get('/api/analytics/violations')
def get_violation_analytics():
    with get_session() as s:
        total_challans = len(s.exec(select(Challan)).all())
        total_revenue = sum([c.amount for c in s.exec(select(Challan)).all()])
        
        return {
            "total_violations": total_challans,
            "total_revenue": total_revenue,
            "avg_fine": total_revenue / total_challans if total_challans > 0 else 0,
            "cameras_count": len(s.exec(select(Camera)).all())
        }

@app.get('/api/analytics/camera/{camera_id}')
def get_camera_analytics(camera_id: int):
    with get_session() as s:
        challans = s.exec(select(Challan).where(Challan.camera_id == camera_id)).all()
        return {
            "camera_id": camera_id,
            "total_violations": len(challans),
            "total_revenue": sum([c.amount for c in challans])
        }

# Vehicle Lookup
@app.get('/api/vehicle/{vehicle_number}')
def lookup_vehicle(vehicle_number: str):
    with get_session() as s:
        challans = s.exec(select(Challan).where(Challan.vehicle == vehicle_number)).all()
        return {
            "vehicle": vehicle_number,
            "total_challans": len(challans),
            "total_fines": sum([c.amount for c in challans]),
            "history": [{
                "id": c.id, 
                "camera_id": c.camera_id, 
                "amount": c.amount,
                "status": c.status,
                "issued_at": c.issued_at
            } for c in challans]
        }

# ==================== NEW FUNCTIONS ====================

# 1. User Profile Management
@app.get('/api/user/{user_id}')
def get_user_profile(user_id: int):
    """Get user profile details"""
    with get_session() as s:
        user = s.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's challans
        challans = s.exec(select(Challan).where(Challan.user_id == user_id)).all()
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "cnic": user.cnic,
            "role": user.role,
            "created_at": user.created_at,
            "last_login": user.last_login,
            "total_challans": len(challans),
            "total_fines": sum([c.amount for c in challans]),
            "unpaid_challans": len([c for c in challans if c.status == "unpaid"])
        }

@app.put('/api/user/{user_id}')
def update_user_profile(user_id: int, full_name: Optional[str] = None, 
                       phone: Optional[str] = None, cnic: Optional[str] = None):
    """Update user profile"""
    with get_session() as s:
        user = s.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if full_name is not None:
            user.full_name = full_name
        if phone is not None:
            user.phone = phone
        if cnic is not None:
            user.cnic = cnic
        
        s.commit()
        s.refresh(user)
        return {"success": True, "user": user}

# 2. Challan History & Search
@app.get('/api/challans')
def get_all_challans(
    status: Optional[str] = None,
    vehicle: Optional[str] = None,
    camera_id: Optional[int] = None,
    user_id: Optional[int] = None,
    limit: int = 100
):
    """Get challans with filtering options"""
    with get_session() as s:
        query = select(Challan)
        
        if status:
            query = query.where(Challan.status == status)
        if vehicle:
            query = query.where(Challan.vehicle.contains(vehicle))
        if camera_id:
            query = query.where(Challan.camera_id == camera_id)
        if user_id:
            query = query.where(Challan.user_id == user_id)
        
        challans = s.exec(query.limit(limit)).all()
        
        return {
            "count": len(challans),
            "challans": [{
                "id": c.id,
                "vehicle": c.vehicle,
                "camera_id": c.camera_id,
                "amount": c.amount,
                "status": c.status,
                "violation_type": c.violation_type,
                "issued_at": c.issued_at,
                "description": c.description
            } for c in challans]
        }

@app.get('/api/challan/{challan_id}')
def get_challan_details(challan_id: int):
    """Get detailed challan information"""
    with get_session() as s:
        challan = s.get(Challan, challan_id)
        if not challan:
            raise HTTPException(status_code=404, detail="Challan not found")
        
        # Get camera info
        camera = s.get(Camera, challan.camera_id)
        
        # Get payment if exists
        payment = s.exec(select(Payment).where(Payment.challan_id == challan_id)).first()
        
        # Get appeal if exists
        appeal = s.exec(select(Appeal).where(Appeal.challan_id == challan_id)).first()
        
        return {
            "challan": {
                "id": challan.id,
                "vehicle": challan.vehicle,
                "amount": challan.amount,
                "status": challan.status,
                "violation_type": challan.violation_type,
                "issued_at": challan.issued_at,
                "description": challan.description,
                "image_url": challan.image_url
            },
            "camera": {
                "id": camera.id if camera else None,
                "address": camera.address if camera else None,
                "lat": camera.lat if camera else None,
                "lng": camera.lng if camera else None
            } if camera else None,
            "payment": {
                "id": payment.id,
                "amount": payment.amount,
                "method": payment.payment_method,
                "status": payment.status,
                "completed_at": payment.completed_at
            } if payment else None,
            "appeal": {
                "id": appeal.id,
                "reason": appeal.reason,
                "status": appeal.status,
                "created_at": appeal.created_at
            } if appeal else None
        }

# 3. Payment Processing
@app.post('/api/payment')
def create_payment(challan_id: int, user_id: int, payment_method: str, 
                  transaction_id: Optional[str] = None):
    """Create a payment for a challan"""
    with get_session() as s:
        challan = s.get(Challan, challan_id)
        if not challan:
            raise HTTPException(status_code=404, detail="Challan not found")
        
        if challan.status == "paid":
            raise HTTPException(status_code=400, detail="Challan already paid")
        
        payment = Payment(
            challan_id=challan_id,
            user_id=user_id,
            amount=challan.amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            status="pending",
            created_at=datetime.now().isoformat()
        )
        
        s.add(payment)
        s.commit()
        s.refresh(payment)
        
        return {"success": True, "payment_id": payment.id}

@app.put('/api/payment/{payment_id}/confirm')
def confirm_payment(payment_id: int):
    """Confirm a payment (admin or payment gateway callback)"""
    with get_session() as s:
        payment = s.get(Payment, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        payment.status = "completed"
        payment.completed_at = datetime.now().isoformat()
        
        # Update challan status
        challan = s.get(Challan, payment.challan_id)
        if challan:
            challan.status = "paid"
            challan.paid_at = datetime.now().isoformat()
        
        s.commit()
        
        return {"success": True, "payment": payment}

@app.get('/api/payments')
def get_payments(user_id: Optional[int] = None, status: Optional[str] = None):
    """Get payment history"""
    with get_session() as s:
        query = select(Payment)
        
        if user_id:
            query = query.where(Payment.user_id == user_id)
        if status:
            query = query.where(Payment.status == status)
        
        payments = s.exec(query).all()
        
        return {
            "count": len(payments),
            "payments": [{
                "id": p.id,
                "challan_id": p.challan_id,
                "amount": p.amount,
                "method": p.payment_method,
                "status": p.status,
                "created_at": p.created_at,
                "completed_at": p.completed_at
            } for p in payments]
        }

# 4. Appeals System
@app.post('/api/appeal')
def create_appeal(challan_id: int, user_id: int, reason: str):
    """Submit an appeal for a challan"""
    with get_session() as s:
        challan = s.get(Challan, challan_id)
        if not challan:
            raise HTTPException(status_code=404, detail="Challan not found")
        
        # Check if appeal already exists
        existing = s.exec(select(Appeal).where(Appeal.challan_id == challan_id)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Appeal already submitted")
        
        appeal = Appeal(
            challan_id=challan_id,
            user_id=user_id,
            reason=reason,
            status="pending",
            created_at=datetime.now().isoformat()
        )
        
        s.add(appeal)
        
        # Update challan status
        challan.status = "appealed"
        
        s.commit()
        s.refresh(appeal)
        
        return {"success": True, "appeal_id": appeal.id}

@app.get('/api/appeals')
def get_appeals(status: Optional[str] = None, user_id: Optional[int] = None):
    """Get appeals list (for admin or user)"""
    with get_session() as s:
        query = select(Appeal)
        
        if status:
            query = query.where(Appeal.status == status)
        if user_id:
            query = query.where(Appeal.user_id == user_id)
        
        appeals = s.exec(query).all()
        
        result = []
        for appeal in appeals:
            challan = s.get(Challan, appeal.challan_id)
            result.append({
                "id": appeal.id,
                "challan_id": appeal.challan_id,
                "vehicle": challan.vehicle if challan else None,
                "amount": challan.amount if challan else None,
                "reason": appeal.reason,
                "status": appeal.status,
                "created_at": appeal.created_at,
                "reviewed_at": appeal.reviewed_at,
                "reviewer_notes": appeal.reviewer_notes
            })
        
        return {"count": len(result), "appeals": result}

@app.put('/api/appeal/{appeal_id}/review')
def review_appeal(appeal_id: int, approved: bool, reviewer_notes: Optional[str] = None):
    """Review an appeal (admin only)"""
    with get_session() as s:
        appeal = s.get(Appeal, appeal_id)
        if not appeal:
            raise HTTPException(status_code=404, detail="Appeal not found")
        
        appeal.status = "approved" if approved else "rejected"
        appeal.reviewed_at = datetime.now().isoformat()
        appeal.reviewer_notes = reviewer_notes
        
        # Update challan status
        challan = s.get(Challan, appeal.challan_id)
        if challan:
            if approved:
                challan.status = "dismissed"
            else:
                challan.status = "unpaid"  # Back to unpaid if appeal rejected
        
        s.commit()
        
        return {"success": True, "appeal": appeal}

# 5. Enhanced Analytics
@app.get('/api/analytics/dashboard')
def get_dashboard_analytics():
    """Get comprehensive dashboard statistics"""
    with get_session() as s:
        all_challans = s.exec(select(Challan)).all()
        all_cameras = s.exec(select(Camera)).all()
        all_payments = s.exec(select(Payment)).all()
        all_appeals = s.exec(select(Appeal)).all()
        
        total_revenue = sum([c.amount for c in all_challans])
        paid_revenue = sum([c.amount for c in all_challans if c.status == "paid"])
        pending_revenue = sum([c.amount for c in all_challans if c.status == "unpaid"])
        
        return {
            "total_violations": len(all_challans),
            "total_revenue": total_revenue,
            "paid_revenue": paid_revenue,
            "pending_revenue": pending_revenue,
            "cameras_count": len(all_cameras),
            "active_cameras": len([c for c in all_cameras if c.status == "active"]),
            "total_payments": len(all_payments),
            "successful_payments": len([p for p in all_payments if p.status == "completed"]),
            "total_appeals": len(all_appeals),
            "pending_appeals": len([a for a in all_appeals if a.status == "pending"]),
            "avg_fine": total_revenue / len(all_challans) if all_challans else 0,
            "violation_types": _count_violation_types(all_challans)
        }

def _count_violation_types(challans):
    """Helper to count violation types"""
    types = {}
    for c in challans:
        vtype = c.violation_type or "unknown"
        types[vtype] = types.get(vtype, 0) + 1
    return types

# 6. Search Functionality
@app.get('/api/search')
def search_all(query: str):
    """Universal search across vehicles, challans, and cameras"""
    with get_session() as s:
        results = {
            "vehicles": [],
            "challans": [],
            "cameras": []
        }
        
        # Search vehicles
        vehicle_challans = s.exec(
            select(Challan).where(Challan.vehicle.contains(query))
        ).all()
        
        vehicles = {}
        for c in vehicle_challans:
            if c.vehicle not in vehicles:
                vehicles[c.vehicle] = {
                    "vehicle": c.vehicle,
                    "total_challans": 0,
                    "total_fines": 0
                }
            vehicles[c.vehicle]["total_challans"] += 1
            vehicles[c.vehicle]["total_fines"] += c.amount
        
        results["vehicles"] = list(vehicles.values())
        
        # Search challans by ID
        try:
            challan_id = int(query)
            challan = s.get(Challan, challan_id)
            if challan:
                results["challans"].append({
                    "id": challan.id,
                    "vehicle": challan.vehicle,
                    "amount": challan.amount,
                    "status": challan.status
                })
        except ValueError:
            pass
        
        # Search cameras by address
        cameras = s.exec(
            select(Camera).where(Camera.address.contains(query))
        ).all()
        
        results["cameras"] = [{
            "id": c.id,
            "address": c.address,
            "status": c.status,
            "total_violations": c.total_violations
        } for c in cameras]
        
        return results

# 7. Camera Health Monitoring
@app.get('/api/cameras/health')
def get_camera_health():
    """Get health status of all cameras"""
    with get_session() as s:
        cameras = s.exec(select(Camera)).all()
        
        health_report = []
        for cam in cameras:
            health_report.append({
                "id": cam.id,
                "address": cam.address,
                "status": cam.status,
                "health_score": cam.health_score,
                "last_maintenance": cam.last_maintenance,
                "total_violations": cam.total_violations,
                "needs_maintenance": cam.health_score < 70
            })
        
        return {
            "total_cameras": len(cameras),
            "healthy": len([c for c in cameras if c.health_score >= 80]),
            "warning": len([c for c in cameras if 50 <= c.health_score < 80]),
            "critical": len([c for c in cameras if c.health_score < 50]),
            "cameras": health_report
        }

@app.put('/api/camera/{camera_id}/maintenance')
def record_maintenance(camera_id: int):
    """Record maintenance for a camera"""
    with get_session() as s:
        camera = s.get(Camera, camera_id)
        if not camera:
            raise HTTPException(status_code=404, detail="Camera not found")
        
        camera.last_maintenance = datetime.now().isoformat()
        camera.health_score = 100  # Reset health score
        
        s.commit()
        
        return {"success": True, "camera": camera}

# 8. Export Reports
@app.get('/api/export/challans-csv')
def export_challans_csv():
    """Export all challans as CSV data"""
    with get_session() as s:
        challans = s.exec(select(Challan)).all()
        
        csv_data = "ID,Vehicle,Camera ID,Amount,Status,Violation Type,Issued At\n"
        for c in challans:
            csv_data += f"{c.id},{c.vehicle},{c.camera_id},{c.amount},{c.status},{c.violation_type},{c.issued_at}\n"
        
        return {"csv": csv_data, "filename": f"challans_export_{datetime.now().strftime('%Y%m%d')}.csv"}

# 9. System Info
@app.get('/api/system/info')
def get_system_info():
    """Get system and GPU status"""
    return get_device_info()