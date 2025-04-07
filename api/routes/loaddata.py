# from fastapi import APIRouter, File, UploadFile, HTTPException, Depends,Query
# from pydantic import BaseModel
# import pyotp
# import pandas as pd
# import io
# from sqlalchemy.orm import Session  # ✅ Add this import
# from sqlalchemy import insert


# from database import get_db  # ✅ Import DB session dependency
# from models import videos 

# router = APIRouter()  # ✅ Define the router

# # Sample MFA Secret (in real scenarios, store this securely per user)
# MFA_SECRET = "JBSWY3DPEHPK3PXP"
# TOTP = pyotp.TOTP(MFA_SECRET, interval=40)  # ✅ Set expiry to 40 seconds

# class MFAVerifyRequest(BaseModel):
#     token: str

# @router.get("/mfa/generate")
# async def generate_otp():
#     """Generates a one-time password (OTP) for MFA."""
#     otp = TOTP.now()  # ✅ Generate OTP with 40-second expiry
#     return {"otp": otp, "expires_in": 40}

# def verify_mfa(token: str = Query(..., description="MFA Token")):
#     """Verifies the MFA token before allowing the request."""
#     if not TOTP.verify(token):
#         raise HTTPException(status_code=401, detail="Invalid MFA token")

# @router.post("/mfa/verify")
# async def verify_mfa_endpoint(request: MFAVerifyRequest):
#     verify_mfa(request.token)
#     return {"message": "MFA verification successful"}


# def parse_datetime(date_str):
#     """Try to parse date in multiple formats"""
#     for fmt in ("%d-%m-%Y %H:%M", "%Y-%m-%d %H:%M"):
#         try:
#             return pd.to_datetime(date_str, format=fmt).strftime("%Y-%m-%d %H:%M:%S")
#         except ValueError:
#             continue
#     raise ValueError(f"Invalid date format: {date_str}")

# @router.post("/upload-data")
# async def upload_data(
#     file: UploadFile = File(...), 
#     token: str = Depends(verify_mfa),
#     db: Session = Depends(get_db)
# ):
#     try:
#         contents = await file.read()

#         # ✅ Read CSV with auto-detect encoding
#         try:
#             df = pd.read_csv(io.BytesIO(contents), encoding="utf-8")
#         except UnicodeDecodeError:
#             df = pd.read_csv(io.BytesIO(contents), encoding="latin1")

#         # ✅ Check if the file is empty
#         if df.empty:
#             raise HTTPException(status_code=400, detail="Uploaded file is empty")

#         # ✅ Validate required columns
#         required_columns = {"file_name", "video_url", "title", "description", "category", "uploaded_by", "created_at"}
#         if not required_columns.issubset(df.columns):
#             raise HTTPException(status_code=400, detail=f"Missing required columns: {required_columns - set(df.columns)}")

#         # ✅ Convert `created_at` to MySQL datetime format
#         df["created_at"] = df["created_at"].apply(parse_datetime)

#         # ✅ Insert rows into the database using bulk insert
#         insert_data = df.to_dict(orient="records")
#         stmt = insert(videos).values(insert_data)
#         db.execute(stmt)
#         db.commit()

#         return {"message": "File processed successfully", "rows": len(df)}
    
#     except ValueError as ve:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=str(ve))

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
#     finally:
#         db.close()