"""
E2E Test: Authentication Flow
signup → login → select-child → kid token validation
"""
import uuid
from tests.conftest import TEST_EMAIL, TEST_PASSWORD, TEST_RUN_ID


class TestAuthFlow:
    """Full authentication lifecycle."""

    async def test_signup_creates_family(self, client, mock_email_service):
        """POST /v1/auth/signup → 201 with family_id."""
        email = f"signup_{TEST_RUN_ID}_{uuid.uuid4().hex[:6]}@example.com"
        resp = await client.post("/v1/auth/signup", json={
            "parent_name": "Signup Test",
            "email": email,
            "password": "StrongPass123!",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "family_id" in data

    async def test_signup_duplicate_email_rejected(self, client, seed_family):
        """Duplicate email → 409."""
        resp = await client.post("/v1/auth/signup", json={
            "parent_name": "Dup Test",
            "email": TEST_EMAIL,
            "password": "AnyPass123!",
        })
        assert resp.status_code == 409

    async def test_login_success(self, client, seed_family):
        """POST /v1/auth/login → 200 with access_token + cookie."""
        resp = await client.post("/v1/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["family_id"] is not None
        # Cookie should be set
        assert "access_token" in resp.cookies or any(
            "access_token" in str(h) for h in resp.headers.get_list("set-cookie")
        )

    async def test_login_wrong_password(self, client, seed_family):
        """Wrong password → 401."""
        resp = await client.post("/v1/auth/login", json={
            "email": TEST_EMAIL,
            "password": "WrongPassword!",
        })
        assert resp.status_code == 401

    async def test_login_nonexistent_email(self, client):
        """Non-existent email → 401."""
        resp = await client.post("/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "AnyPass!",
        })
        assert resp.status_code == 401

    async def test_select_child_success(self, client, seed_family, family_token):
        """POST /v1/auth/select-child → child_token."""
        resp = await client.post("/v1/auth/select-child", json={
            "child_id": seed_family["child_id"],
        }, headers={"Authorization": f"Bearer {family_token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert "child_token" in data
        assert data["child_name"] is not None

    async def test_select_child_wrong_family(self, client, seed_family):
        """Selecting a child from a different family → 401."""
        fake_token = __import__("app.core.security", fromlist=["create_access_token"]).create_access_token(
            {"family_id": str(uuid.uuid4())}
        )
        resp = await client.post("/v1/auth/select-child", json={
            "child_id": seed_family["child_id"],
        }, headers={"Authorization": f"Bearer {fake_token}"})
        assert resp.status_code == 401

    async def test_select_child_no_auth(self, client, seed_family):
        """No auth header → 401."""
        resp = await client.post("/v1/auth/select-child", json={
            "child_id": seed_family["child_id"],
        })
        assert resp.status_code == 401
