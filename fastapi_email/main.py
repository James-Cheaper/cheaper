from fastapi import FastAPI, HTTPException, Depends
from fastapi_email.schemas import EmailSchema
from fastapi_email.database import engine, Base, get_db
from fastapi_email.models import User
from fastapi_email.utils import generate_token, send_verification_email, send_confirmation_email
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/register")
async def register(data: EmailSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        if existing.is_verified:
            raise HTTPException(400, detail="Email already verified")
        else:
            existing.token = generate_token()
            existing.token_expiry = datetime.utcnow() + timedelta(minutes=15)
            db.commit()
            await send_verification_email(existing.email, existing.token)
            return {"message": "Verification email re-sent"}

    token = generate_token()
    expiry_time = datetime.utcnow() + timedelta(minutes=15)

    new_user = User(email=data.email, token=token, token_expiry=expiry_time, is_verified=False)
    db.add(new_user)
    db.commit()
    await send_verification_email(data.email, token)
    return {"message": "Verification email sent"}


@app.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(400, detail="Invalid token")

    if user.token_expiry and datetime.utcnow() > user.token_expiry:
        raise HTTPException(400, detail="Verification link has expired")

    user.is_verified = True
    user.token = None
    user.token_expiry = None
    db.commit()
    await send_confirmation_email(user.email)
    return {"message": "Email verified"}


@app.get("/status/{email}")
def check_status(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": email, "is_verified": user.is_verified}
