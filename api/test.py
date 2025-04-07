import pyotp
import datetime, pyotp
secret = "7T3E3DGS75HVQITS2QPZBONJWXUCJ7DK"  # Use your secret from DB
# totp = pyotp.TOTP(secret)

# print("Current OTP:", totp.now())



print("Server time:", datetime.datetime.now())
print("Expected OTP:", pyotp.TOTP(secret).now())