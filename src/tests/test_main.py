from unittest.mock import patch
from sqlmodel import Session, SQLModel, create_engine
from app.database import get_session
from app.models import Season


NOT_AUTHENTICATED = {"detail": "Not authenticated"}

def test_ping(test_client):
    response = test_client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}

#def test_get_misconducts_empty(test_app):
#    response = test_app.get("/misconducts")
#    assert response.status_code == 200
#    assert response.json() == []

#def test_post_misconducts(test_app):
#    response = test_app.post("/misconducts")
#    assert response.status_code == 201
#    assert response.json() == {"ping": "pong!"}

def test_post_misconducts_not_authenticated(test_client):
    response = test_client.post("/misconduct")
    assert response.status_code == 401
    assert response.json() == NOT_AUTHENTICATED
