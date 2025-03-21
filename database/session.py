from contextlib import asynccontextmanager
import logging
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env file")

# Create an async engine
engine = create_async_engine(DATABASE_URL)

# Set up logging once when the module is loaded
logging.basicConfig(level=logging.WARNING)  # Set the default logging level
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)  # SQLAlchemy engine to WARNING

# Async session maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Dependency to get an async session
@asynccontextmanager
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
