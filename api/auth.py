import os
from jose import jwt  # Use `python-jose`
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose.exceptions import JWTError 
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

# Function to Hash Password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to Verify Password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to Generate JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    # Convert 'sub' (subject) to a string
    to_encode["sub"] = str(to_encode["sub"])  

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to Decode JWT Token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:  # Corrected from InvalidTokenError to JWTError
        raise HTTPException(status_code=401, detail="Invalid token")

# Function to Get Current Admin from Token
def get_current_admin(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    admin_id: int = payload.get("sub")
    if admin_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return admin_id
