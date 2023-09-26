import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from config.database import Base, engine, get_db
from config.settings import Settings, get_settings
from main import app
from models.sqlmodels import User
from utils.hasher import HasherJwt

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def create_test_table_end_remove_after_test():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db(create_test_table_end_remove_after_test) -> Session:
    return TestingSessionLocal()


@pytest.fixture
def auth_client(client: TestClient, db: Session):
    user = User(username="test")
    user.make_password("test")
    db.add(user)
    db.commit()
    settings = get_settings()
    hasher = HasherJwt(
        algorithm=settings.algorytm,
        secret=settings.token_secret,
    )
    token = hasher.make_secret(user.public_id)
    client.headers = {"Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def settings() -> Settings:
    return get_settings()
