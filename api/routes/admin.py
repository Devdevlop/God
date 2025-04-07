from fastapi import APIRouter, Depends, HTTPException
from auth import create_access_token, verify_password, hash_password, get_current_admin
from database import database
from models import admin_users
from datetime import timedelta
from schemas import AdminLogin
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from datetime import timedelta
from jose import JWTError

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Admin Login Route

@router.post("/admin/login")
async def admin_login(data: AdminLogin):
    try:
        # ✅ Fetch admin user from the database
        query = admin_users.select().where(admin_users.c.username == data.username)
        result = await database.fetch_one(query)

        # ✅ Ensure result is valid and convert to dictionary
        if result:
            admin = dict(result)  # ✅ Convert to dictionary if needed
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # ✅ Ensure the user has a valid password hash
        if "password_hash" not in admin or not verify_password(data.password, admin["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # ✅ Check if MFA is enabled for the user
        if "mfa_enabled" in admin and admin["mfa_enabled"]:
            return {"mfa_required": True, "username": admin["username"]}  # ✅ Frontend should request OTP

        # ✅ If MFA is NOT required, generate a JWT token and return it
        access_token = create_access_token(
            data={"sub": admin["id"]}, expires_delta=timedelta(minutes=30)
        )
        return {"access_token": access_token, "token_type": "bearer"}

    except SQLAlchemyError as db_error:
        print(f"Database error: {db_error}")  # ✅ Log database errors
        raise HTTPException(status_code=500, detail="Database error. Please try again later.")

    except HTTPException as http_error:
        raise http_error  # ✅ Directly raise HTTP exceptions (e.g., invalid login)

    except Exception as e:
        print(f"Unexpected error: {e}")  # ✅ Log unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")  # ✅ Return exact error for debugging
# Protected Route (Requires JWT)
@router.get("/admin/protected")
async def protected_route(admin_id: int = Depends(get_current_admin)):
    try:
        if not admin_id:
            raise HTTPException(status_code=401, detail="Invalid authentication")

        return {"message": f"Hello Admin {admin_id}, you have access!"}

    except HTTPException as http_error:
        # This will handle authentication and authorization errors
        raise http_error  # Re-raise FastAPI exceptions for proper handling

    except SQLAlchemyError as db_error:
        # Handle database errors (in case you expand this function later)
        print(f"Database error: {db_error}")  # Log the error (use proper logging in production)
        raise HTTPException(status_code=500, detail="Database error. Please try again later.")

    except JWTError:
        # Handle JWT token decoding errors
        raise HTTPException(status_code=401, detail="Invalid token. Please log in again.")

    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error: {e}")  # Log the error (use proper logging in production)
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please contact support.")