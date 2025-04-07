from sqlalchemy import Table, Column, Integer, String, ForeignKey,Boolean, TIMESTAMP, Enum, Text, text
from database import metadata

# ✅ Admin Users Table (Updated with `mfa_secret`)
admin_users = Table(
    "admin_users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(50), unique=True, nullable=False),
    Column("password_hash", String(255), nullable=False),
    Column("email", String(100), unique=True, nullable=False),
    Column("role", Enum("superadmin", "editor", "moderator"), server_default=text("'editor'")),  # ✅ Fixed Default Value
    Column("mfa_secret", String(255), nullable=True),  # ✅ MFA Secret Column
    Column("mfa_enabled", Boolean, server_default=text("0"), nullable=False),  # ✅ Added MFA Enabled (BOOLEAN as TINYINT(1))
    Column("created_at", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
)

# ✅ Images Table
images = Table(
    "images", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("file_name", String(255), nullable=False),
    Column("image_url", String(255), nullable=False),
    Column("alt_text", String(255), nullable=True),
    Column("category", String(100), nullable=True),
    Column("uploaded_by", Integer, ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True),  # ✅ Ensured ON DELETE SET NULL
    Column("created_at", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),  # ✅ Auto-update timestamp
)

# ✅ Videos Table
videos = Table(
    "videos", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("file_name", String(255), nullable=False),
    Column("video_url", String(255), nullable=False),
    Column("title", String(255), nullable=True),
    Column("description", Text, nullable=True),
    Column("category", String(100), nullable=True),
    Column("uploaded_by", Integer, ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True),  # ✅ Ensured ON DELETE SET NULL
    Column("created_at", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),  # ✅ Auto-update timestamp
)
