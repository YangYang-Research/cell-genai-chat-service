import secrets
from sqlalchemy import text
from helpers.loog import logger
from urllib.parse import urlparse
from sqlalchemy.orm import sessionmaker
from helpers.config import AppConfig, DatabaseConfig
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from helpers.secret import AWSSecretManager
from databases.models import RoleModel, UserModel, ToolConfigModel
from sqlalchemy.future import select
from passlib.context import CryptContext

app_conf = AppConfig()
db_conf = DatabaseConfig()
aws_secret_manager = AWSSecretManager()

db_username = aws_secret_manager.get_secret(db_conf.db_username_key)
db_pwd = aws_secret_manager.get_secret(db_conf.db_pwd_key)

DATABASE_URL = f"postgresql+asyncpg://{db_username}:{db_pwd}@{db_conf.db_host}:{db_conf.db_port}/{db_conf.db_name}"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

async def seed_role(session):
    """Initialize default role."""
    result = await session.execute(select(RoleModel))
    existing_roles = result.scalars().all()

    if not existing_roles:
        roles = [
            RoleModel(name="admin", description="Administrator with full access"),
            RoleModel(name="user", description="Standard user with limited permissions"),
        ]
        session.add_all(roles)
        await session.commit()
        logger.info("✅ Roles initialized")

async def seed_admin(session):
    """Initialize default admin user."""
    result = await session.execute(select(UserModel).where(UserModel.username == "administrator"))
    admin = result.scalars().first()

    if admin:
        logger.info("👤 Default admin user already exists.")
        return

    # Get admin role
    sql_role = await session.execute(select(RoleModel).where(RoleModel.name == "admin"))
    admin_role = sql_role.scalars().first()
    
    init_admin_password = secrets.token_hex(16)

    admin_user = UserModel(
        username="administrator",
        email=app_conf.app_admin_email,
        hashed_password=pwd_context.hash(init_admin_password),
        full_name="Administrator",
        role_id=admin_role.id
    )

    session.add(admin_user)
    await session.commit()
    logger.info(f"✅ Created default admin user: {app_conf.app_admin_email}")
    logger.info(f"✅ Created default admin password: {init_admin_password}")

async def seed_tool_config(session):
    tools = [
        {"name": "duckduckgo", "status": "enable"},
        {"name": "arxiv", "status": "enable"},
        {"name": "wikipedia", "status": "enable"},
        {"name": "google_search", "status": "disable"},
        {"name": "google_scholar", "status": "disable"},
        {"name": "google_trend", "status": "disable"},
        {"name": "asknews", "status": "disable"},
        {"name": "reddit", "status": "disable"},
        {"name": "searx", "status": "disable"},
        {"name": "openweather", "status": "disable"},
    ]

    for t in tools:
        result = await session.execute(select(ToolConfigModel).where(ToolConfigModel.name == t["name"]))
        existing = result.scalars().first()
        if not existing:
            session.add(ToolConfigModel(**t))

    await session.commit()
    logger.info("✅ ToolConfig seeded successfully")


async def seed_initial_data(session):
    await seed_role(session)
    await seed_admin(session)
    await seed_tool_config(session)