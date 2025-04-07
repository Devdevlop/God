from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "Mango@22"  # Replace with your real password
hashed_password = pwd_context.hash(password)

print("Hashed Password:", hashed_password)
