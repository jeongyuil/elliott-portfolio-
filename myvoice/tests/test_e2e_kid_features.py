"""
E2E Test: Kid Features
home → adventures → vocabulary → shop → profile → skills → goals
"""


class TestKidHome:
    """Kid home endpoint."""

    async def test_kid_home(self, client, child_token):
        """GET /v1/kid/home → home dashboard data."""
        resp = await client.get(
            "/v1/kid/home",
            headers={"Authorization": f"Bearer {child_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        # Should have child profile info
        assert "child" in data or "name" in data or "streak" in data

    async def test_kid_home_no_auth(self, client):
        """Kid home without auth → 401."""
        resp = await client.get("/v1/kid/home")
        assert resp.status_code == 401



class TestKidAdventures:
    """Kid adventures (curriculum units) endpoints."""

    async def test_list_adventures(self, client, child_token):
        """GET /v1/kid/adventures → adventure list."""
        resp = await client.get(
            "/v1/kid/adventures",
            headers={"Authorization": f"Bearer {child_token}"},
        )
        # May return 200 with empty list if no curriculum seeded
        assert resp.status_code == 200



class TestKidVocabulary:
    """Kid vocabulary endpoints."""

    async def test_list_categories(self, client, child_token):
        """GET /v1/kid/vocabulary → category list."""
        resp = await client.get(
            "/v1/kid/vocabulary",
            headers={"Authorization": f"Bearer {child_token}"},
        )
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)



class TestKidShop:
    """Kid shop endpoints."""

    async def test_shop_items(self, client, child_token):
        """GET /v1/kid/shop → items + inventory."""
        resp = await client.get(
            "/v1/kid/shop",
            headers={"Authorization": f"Bearer {child_token}"},
        )
        assert resp.status_code == 200



class TestKidProfile:
    """Kid profile endpoint."""

    async def test_get_profile(self, client, child_token):
        """GET /v1/kid/profile → child profile data."""
        resp = await client.get(
            "/v1/kid/profile",
            headers={"Authorization": f"Bearer {child_token}"},
        )
        assert resp.status_code == 200



class TestKidSkills:
    """Kid skills endpoint."""

    async def test_get_skills(self, client, child_token):
        """GET /v1/kid/skills → skill levels."""
        resp = await client.get(
            "/v1/kid/skills",
            headers={"Authorization": f"Bearer {child_token}"},
        )
        assert resp.status_code == 200



class TestKidGoals:
    """Kid goals endpoint."""

    async def test_get_goals(self, client, child_token):
        """GET /v1/kid/goals → weekly goals."""
        resp = await client.get(
            "/v1/kid/goals",
            headers={"Authorization": f"Bearer {child_token}"},
        )
        assert resp.status_code == 200
