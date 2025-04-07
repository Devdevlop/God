import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import database, metadata, engine
import routes.media
import routes.admin
import routes.loaddata
import routes.mfa

# ✅ Global Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ✅ API Metadata
app = FastAPI(
    title="Video Management API",
    description="APIs for managing video uploads, authentication, and data handling",
    version="1.0.0",
    contact={"name": "Your Name", "email": "your@email.com"},
)

# ✅ Create Database Tables
metadata.create_all(engine)

# ✅ CORS Middleware (Fixes React API request issue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ✅ Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Global Exception Logging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"⚠️ Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )

# ✅ Database Connection Events
@app.on_event("startup")
async def startup():
    await database.connect()
    logger.info("✅ Database Connected Successfully")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info("❌ Database Disconnected")

# ✅ Include All API Routers
app.include_router(routes.media.router, prefix="/api")
app.include_router(routes.admin.router, prefix="/api")
# app.include_router(routes.loaddata.router, prefix="/api")
app.include_router(routes.mfa.router, prefix="/api")







# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from database import database, metadata, engine
# import routes.media
# import routes.admin
# import routes.loaddata
# import routes.mfa


# # ✅ API Metadata
# app = FastAPI(
#     title="Video Management API",
#     description="APIs for managing video uploads, authentication, and data handling",
#     version="1.0.0",
#     contact={"name": "Your Name", "email": "your@email.com"},
# )

# # ✅ Create Database Tables
# metadata.create_all(engine)

# # ✅ CORS Middleware (Fixes React API request issue)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # ✅ Allow React frontend
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Handle Unexpected Errors Globally
# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     print(f"⚠️ Unexpected error: {exc}")  # ✅ Log error in terminal
#     return JSONResponse(
#         status_code=500,
#         content={"detail": "An unexpected error occurred. Please try again later."},
#     )

# # ✅ Database Connection Events
# @app.on_event("startup")
# async def startup():
#     await database.connect()
#     print("✅ Database Connected Successfully")

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
#     print("❌ Database Disconnected")

# # ✅ Include API Routes
# app.include_router(routes.media.router, prefix="/api")
# app.include_router(routes.admin.router, prefix="/api")
# app.include_router(routes.loaddata.router, prefix="/api")
# app.include_router(routes.mfa.router, prefix="/api")
