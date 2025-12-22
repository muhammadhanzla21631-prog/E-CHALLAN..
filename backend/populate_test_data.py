import hashlib
from datetime import datetime, timedelta
from sqlmodel import Session, select
from db import engine, init_db
from models import Camera, User, Challan, Payment, Appeal

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def populate():
    init_db()
    with Session(engine) as session:
        # 1. Cameras
        print("Populating Cameras...")
        cameras = [
            Camera(lat=31.5204, lng=74.3587, address="Mall Road, Lahore", status="active", speed_limit=60),
            Camera(lat=31.5497, lng=74.3436, address="Jail Road, Lahore", status="active", speed_limit=50),
            Camera(lat=31.4805, lng=74.3239, address="Ferozepur Road, Lahore", status="active", speed_limit=70),
            Camera(lat=31.4697, lng=74.2728, address="Canal Road, Lahore", status="active", speed_limit=60),
            Camera(lat=31.5826, lng=74.3290, address="Ring Road, Lahore", status="active", speed_limit=100),
        ]
        
        for cam in cameras:
            # Check if exists
            existing = session.exec(select(Camera).where(Camera.address == cam.address)).first()
            if not existing:
                session.add(cam)
        session.commit()
        
        # Refresh cameras to get IDs
        db_cameras = session.exec(select(Camera)).all()
        cam_ids = [c.id for c in db_cameras]

        # 2. Users
        print("Populating Users...")
        users = [
            User(
                username="admin", 
                email="admin@echallan.com", 
                password_hash=hash_password("admin123"), 
                full_name="System Admin", 
                role="admin",
                created_at=datetime.now().isoformat()
            ),
            User(
                username="hanzla", 
                email="hanzla@example.com", 
                password_hash=hash_password("password123"), 
                full_name="Muhammad Hanzla", 
                phone="03001234567",
                cnic="35202-1234567-1",
                role="user",
                created_at=datetime.now().isoformat()
            )
        ]

        for user in users:
            existing = session.exec(select(User).where(User.username == user.username)).first()
            if not existing:
                session.add(user)
        session.commit()

        # Get User ID for Hanzla
        hanzla = session.exec(select(User).where(User.username == "hanzla")).first()
        
        if not hanzla:
            print("User creation failed.")
            return

        # 3. Challans
        print("Populating Challans...")
        
        # Unpaid
        challans_data = [
            Challan(vehicle="LEC-1234", camera_id=cam_ids[0], amount=500, violation_type="red_light", status="unpaid", user_id=hanzla.id, issued_at=(datetime.now() - timedelta(days=2)).isoformat(), description="Crossed red light at Mall Road"),
            Challan(vehicle="LEC-1234", camera_id=cam_ids[1], amount=200, violation_type="no_helmet", status="unpaid", user_id=hanzla.id, issued_at=(datetime.now() - timedelta(days=5)).isoformat(), description="Riding without helmet"),
            Challan(vehicle="ABC-789", camera_id=cam_ids[2], amount=1000, violation_type="overspeed", status="unpaid", user_id=hanzla.id, issued_at=(datetime.now() - timedelta(days=1)).isoformat(), description="Speed 85km/h in 70km/h zone"),
        ]
        
        # Paid
        paid_challans = [
            Challan(vehicle="LEC-1234", camera_id=cam_ids[3], amount=500, violation_type="red_light", status="paid", user_id=hanzla.id, issued_at=(datetime.now() - timedelta(days=10)).isoformat(), paid_at=(datetime.now() - timedelta(days=9)).isoformat(), description="Crossed red light"),
            Challan(vehicle="LEC-1234", camera_id=cam_ids[0], amount=300, violation_type="wrong_way", status="paid", user_id=hanzla.id, issued_at=(datetime.now() - timedelta(days=15)).isoformat(), paid_at=(datetime.now() - timedelta(days=14)).isoformat(), description="Driving wrong way"),
            Challan(vehicle="XYZ-999", camera_id=cam_ids[4], amount=1000, violation_type="overspeed", status="paid", user_id=hanzla.id, issued_at=(datetime.now() - timedelta(days=20)).isoformat(), paid_at=(datetime.now() - timedelta(days=19)).isoformat(), description="Speed 120km/h in 100km/h zone"),
        ]
        
        # Appealed
        appealed_challans = [
            Challan(vehicle="LEC-1234", camera_id=cam_ids[1], amount=500, violation_type="red_light", status="appealed", user_id=hanzla.id, issued_at=(datetime.now() - timedelta(days=3)).isoformat(), description="Alleged red light violation"),
            Challan(vehicle="ABC-789", camera_id=cam_ids[2], amount=1000, violation_type="overspeed", status="unpaid", user_id=hanzla.id, issued_at=(datetime.now() - timedelta(days=8)).isoformat(), description="Speeding violation rejected appeal"), # Was appealed, now unpaid (rejected)
        ]
        
        all_challans = challans_data + paid_challans + appealed_challans
        
        for c in all_challans:
             # Check duplicates by vehicle and time roughly (simplified)
             existing = session.exec(select(Challan).where(Challan.vehicle == c.vehicle, Challan.issued_at == c.issued_at)).first()
             if not existing:
                 session.add(c)
        session.commit()
        
        # Refresh to get IDs for payments and appeals
        # Add Payments for Paid Challans
        print("Populating Payments...")
        for c in paid_challans:
            # Fetch from DB to get ID
            db_c = session.exec(select(Challan).where(Challan.vehicle == c.vehicle, Challan.issued_at == c.issued_at)).first()
            if db_c:
                # Check if payment exists
                existing_payment = session.exec(select(Payment).where(Payment.challan_id == db_c.id)).first()
                if not existing_payment:
                    payment = Payment(
                        challan_id=db_c.id,
                        user_id=hanzla.id,
                        amount=db_c.amount,
                        payment_method="credit_card",
                        transaction_id=f"TXN-{db_c.id}-12345",
                        status="completed",
                        created_at=db_c.paid_at,
                        completed_at=db_c.paid_at
                    )
                    session.add(payment)
        
        # Add Appeals
        print("Populating Appeals...")
        # Pending Appeal
        c_appeal_pending = appealed_challans[0]
        db_c_pending = session.exec(select(Challan).where(Challan.vehicle == c_appeal_pending.vehicle, Challan.issued_at == c_appeal_pending.issued_at)).first()
        if db_c_pending:
            existing_appeal = session.exec(select(Appeal).where(Appeal.challan_id == db_c_pending.id)).first()
            if not existing_appeal:
                appeal = Appeal(
                    challan_id=db_c_pending.id,
                    user_id=hanzla.id,
                    reason="I was not driving the car at that time.",
                    status="pending",
                    created_at=(datetime.now() - timedelta(days=1)).isoformat()
                )
                session.add(appeal)
            
        # Rejected Appeal
        c_appeal_rejected = appealed_challans[1]
        db_c_rejected = session.exec(select(Challan).where(Challan.vehicle == c_appeal_rejected.vehicle, Challan.issued_at == c_appeal_rejected.issued_at)).first()
        if db_c_rejected:
            existing_appeal = session.exec(select(Appeal).where(Appeal.challan_id == db_c_rejected.id)).first()
            if not existing_appeal:
                appeal = Appeal(
                    challan_id=db_c_rejected.id,
                    user_id=hanzla.id,
                    reason="The speed limit sign was not visible.",
                    status="rejected",
                    created_at=(datetime.now() - timedelta(days=7)).isoformat(),
                    reviewed_at=(datetime.now() - timedelta(days=6)).isoformat(),
                    reviewer_notes="Signage is clearly visible in evidence."
                )
                session.add(appeal)

        session.commit()
        print("Test data populated successfully!")

if __name__ == "__main__":
    populate()
