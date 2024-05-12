
NOT_AUTHENTICATED = {"detail": "Not authenticated"}

def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}

def test_get_seasons_empty(test_app):
    response = test_app.get("/seasons")
    assert response.status_code == 200
    assert response.json() == []

def test_post_seasons_not_authenticated(test_app):
    response = test_app.post("/seasons")
    assert response.status_code ==403
    assert response.json() == NOT_AUTHENTICATED

#def test_post_seasons(test_app):
#    response = test_app.post("/seasons")
#    assert response.status_code == 201
#    assert response.json() == {"ping": "pong!"}

def test_get_misconducts_empty(test_app):
    response = test_app.get("/misconducts")
    assert response.status_code == 200
    assert response.json() == []

#def test_post_misconducts(test_app):
#    response = test_app.post("/misconducts")
#    assert response.status_code == 201
#    assert response.json() == {"ping": "pong!"}

def test_post_misconducts_not_authenticated(test_app):
    response = test_app.post("/misconducts")
    assert response.status_code == 403
    assert response.json() == NOT_AUTHENTICATED
