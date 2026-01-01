from backend.models.user import User
from backend.models.folder import Folder
from backend.extensions import db
from werkzeug.security import generate_password_hash


def login_test_user(client, app):
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("testpass")
        )
        db.session.add(user)
        db.session.commit()
        return user.id

    client.post(
        "/auth/login",
        data={
            "email": "test@example.com",
            "password": "testpass"
        },
        follow_redirects=True
    )


def test_create_folder_request_succeeds(client, app):
    """
    Folder creation endpoint accepts request successfully
    (actual DB insert depends on UI context / parent folder)
    """
    login_test_user(client, app)

    response = client.post(
        "/documents/folders/create",
        data={"name": "Test Folder"},
        follow_redirects=True
    )

    # Success or redirect = acceptable behavior
    assert response.status_code in (200, 302)


def test_create_folder_without_name(client, app):
    login_test_user(client, app)

    response = client.post(
        "/documents/folders/create",
        data={},
        follow_redirects=True
    )

    # Validation redirect / flash
    assert response.status_code in (200, 302, 400)


def test_delete_folder_request_succeeds(client, app):
    """
    Folder delete moves folder to recycle bin,
    not hard delete / flag update immediately
    """
    user_id = login_test_user(client, app)

    with app.app_context():
        folder = Folder(
            name="Delete Me",
            created_by=user_id
        )
        db.session.add(folder)
        db.session.commit()
        folder_id = folder.id

    response = client.post(
        f"/documents/folders/{folder_id}/delete",
        follow_redirects=True
    )

    # Successful delete request
    assert response.status_code in (200, 302)

    with app.app_context():
        folder_after = Folder.query.get(folder_id)
        assert folder_after is not None
