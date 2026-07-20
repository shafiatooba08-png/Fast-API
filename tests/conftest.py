import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.main import app
from app.database.database import Base
from app.customers.router import get_db as customer_get_db
from app.leads.router import get_db as lead_get_db
from app.properties.routes import get_db as property_get_db


# ------------------------------------------------------------------
# In-memory SQLite database
# ------------------------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ------------------------------------------------------------------
# Override database dependency
# ------------------------------------------------------------------

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[customer_get_db] = override_get_db
app.dependency_overrides[lead_get_db] = override_get_db
app.dependency_overrides[property_get_db] = override_get_db


# ------------------------------------------------------------------
# Database fixture
# ------------------------------------------------------------------

@pytest.fixture
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# ------------------------------------------------------------------
# Test client
# ------------------------------------------------------------------

@pytest.fixture
def client(db):
    with TestClient(app) as client:
        yield client