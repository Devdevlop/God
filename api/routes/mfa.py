from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from datetime import datetime
import pyotp, qrcode, io, base64, logging

from database import get_db
from models import admin_users
from auth import create_access_token
from schemas import MFAVerifyRequest  # ✅ Import Pydantic model from schemas.py

router = APIRouter()
logger = logging.getLogger("uvicorn.error")


@router.get("/mfa/generate/{username}")
async def generate_qr(username: str, db: Session = Depends(get_db)):
    logger.info(f"[QR GENERATE] Request received for user: {username}")

    user_query = admin_users.select().where(admin_users.c.username == username)
    user = db.execute(user_query).fetchone()

    if not user:
        logger.warning(f"[QR GENERATE] User not found: {username}")
        raise HTTPException(status_code=404, detail="User not found")

    mfa_secret = user.mfa_secret
    if not mfa_secret:
        mfa_secret = pyotp.random_base32()
        logger.info(f"[QR GENERATE] Generated new MFA secret for user: {username}")

        update_query = (
            admin_users.update()
            .where(admin_users.c.username == username)
            .values(mfa_secret=mfa_secret, mfa_enabled=0)
        )
        db.execute(update_query)
        db.commit()
        logger.info(f"[QR GENERATE] Stored new secret in DB for user: {username}")

    otp_uri = pyotp.TOTP(mfa_secret).provisioning_uri(name=username, issuer_name="MyApp")

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(otp_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
        logger.error(f"[QR GENERATE] QR generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="QR Code generation failed")

    logger.info(f"[QR GENERATE] QR code successfully generated for {username}")
    return {
        "qr_code": qr_base64,
        "mfa_secret": mfa_secret,
        "mfa_enabled": user.mfa_enabled == 1
    }


@router.post("/mfa/verify")
async def verify_mfa_code(request: MFAVerifyRequest, db: Session = Depends(get_db)):
    logger.info("🚨 ENTERED /mfa/verify endpoint")

    try:
        logger.info(f"Username: {request.username}, Token: {request.token}")

        user_query = admin_users.select().where(admin_users.c.username == request.username)
        user = db.execute(user_query).fetchone()

        logger.info(f"DB User: {user}")

        if not user or not user.mfa_secret:
            logger.warning("User not found or MFA secret missing.")
            raise HTTPException(status_code=401, detail="Invalid user or 2FA not initialized")

        totp = pyotp.TOTP(user.mfa_secret)
        expected = totp.now()

        logger.info(f"Server time: {datetime.now()}")
        logger.info(f"Expected OTP: {expected}, Submitted OTP: {request.token}")

        if not totp.verify(request.token, valid_window=1):
            logger.warning("OTP verification failed.")
            raise HTTPException(status_code=401, detail="Invalid OTP")

        logger.info("OTP verified successfully.")

        if not user.mfa_enabled:
            logger.info("Enabling MFA for user...")
            update_query = (
                admin_users.update()
                .where(admin_users.c.username == request.username)
                .values(mfa_enabled=1)
            )
            db.execute(update_query)
            db.commit()
            logger.info("MFA status updated in DB.")

        access_token = create_access_token(data={"sub": user.username})
        logger.info("Access token generated.")

        return {
            "verified": True,
            "access_token": access_token
        }

    except Exception as e:
        logger.exception(f"💥 Exception in /mfa/verify: {e}")
        raise HTTPException(status_code=500, detail="Server error during verification")



@router.post("/mfa/debug")
async def mfa_debug(request: MFAVerifyRequest, db: Session = Depends(get_db)):
    logger.info("🚨 ENTERED /mfa/verify endpoint")

    try:
        logger.info(f"Username: {request.username}, Token: {request.token}")

        user_query = admin_users.select().where(admin_users.c.username == request.username)
        user = db.execute(user_query).fetchone()

        logger.info(f"DB User: {user}")

        if not user or not user.mfa_secret:
            logger.warning("User not found or MFA secret missing.")
            raise HTTPException(status_code=401, detail="Invalid user or 2FA not initialized")

        totp = pyotp.TOTP(user.mfa_secret)
        expected = totp.now()

        logger.info(f"Server time: {datetime.now()}")
        logger.info(f"Expected OTP: {expected}, Submitted OTP: {request.token}")

        if not totp.verify(request.token, valid_window=1):
            logger.warning("OTP verification failed.")
            raise HTTPException(status_code=401, detail="Invalid OTP")

        logger.info("OTP verified successfully.")

        if not user.mfa_enabled:
            logger.info("Enabling MFA for user...")
            update_query = (
                admin_users.update()
                .where(admin_users.c.username == request.username)
                .values(mfa_enabled=1)
            )
            db.execute(update_query)
            db.commit()
            logger.info("MFA status updated in DB.")

        access_token = create_access_token(data={"sub": user.username})
        logger.info("Access token generated.")

        return {
            "verified": True,
            "access_token": access_token
        }

    except Exception as e:
        logger.exception(f"💥 Exception in /mfa/verify: {e}")
        raise HTTPException(status_code=500, detail="Server error during verification")
    # logger.info("🔥 Parsed Request via Pydantic:")
    # logger.info(f"Username: {request.username}")
    # logger.info(f"Token: {request.token}")
    # return {"received": True}

from sqlalchemy import text  # ✅ Add this import

@router.get("/mfa/db-debug")
async def mfa_db_debug(db: Session = Depends(get_db)):
    logger.info("🧪 DB Connection Debug:")
    logger.info(f"DB session object: {db}")
    
    try:
        result = db.execute(text("SELECT 1"))
        logger.info(f"DB Test Query Result: {result.scalar()}")
    except Exception as e:
        logger.error(f"❌ Error testing DB connection: {e}")
        return {"db_connection": False, "error": str(e)}

    return {"db_connection": True}
