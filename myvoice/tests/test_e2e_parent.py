"""
E2E Test: Parent Dashboard Flow
list children → dashboard stats → reports → insights endpoints
"""
class TestParentDashboard:
    """Parent view API flow."""

    async def test_list_children(self, client, family_token, seed_family):
        """GET /v1/parent/children → list with our test child."""
        resp = await client.get(
            "/v1/parent/children",
            headers={"Authorization": f"Bearer {family_token}"},
        )
        assert resp.status_code == 200
        children = resp.json()
        assert isinstance(children, list)
        assert len(children) >= 1
        child_ids = [c["child_id"] for c in children]
        assert seed_family["child_id"] in child_ids

    async def test_get_dashboard_stats(self, client, family_token, seed_family):
        """GET /v1/parent/dashboard/stats → weekly stats."""
        resp = await client.get(
            f"/v1/parent/dashboard/stats?child_id={seed_family['child_id']}",
            headers={"Authorization": f"Bearer {family_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "total_sessions" in data
        assert "total_learning_time_minutes" in data
        assert "daily_breakdown" in data

    async def test_list_reports(self, client, family_token, seed_family):
        """GET /v1/parent/reports → report list (may be empty)."""
        resp = await client.get(
            f"/v1/parent/reports?child_id={seed_family['child_id']}",
            headers={"Authorization": f"Bearer {family_token}"},
        )
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_insights_keywords(self, client, family_token, seed_family):
        """GET /v1/parent/insights/keywords → keyword list."""
        resp = await client.get(
            f"/v1/parent/insights/keywords?child_id={seed_family['child_id']}",
            headers={"Authorization": f"Bearer {family_token}"},
        )
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_insights_sentiment(self, client, family_token, seed_family):
        """GET /v1/parent/insights/sentiment → emotions + overall."""
        resp = await client.get(
            f"/v1/parent/insights/sentiment?child_id={seed_family['child_id']}",
            headers={"Authorization": f"Bearer {family_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "emotions" in data
        assert "overall" in data

    async def test_insights_timeline(self, client, family_token, seed_family):
        """GET /v1/parent/insights/timeline → daily activity list."""
        resp = await client.get(
            f"/v1/parent/insights/timeline?child_id={seed_family['child_id']}",
            headers={"Authorization": f"Bearer {family_token}"},
        )
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_insights_language_mix(self, client, family_token, seed_family):
        """GET /v1/parent/insights/language-mix → Korean/English ratio."""
        resp = await client.get(
            f"/v1/parent/insights/language-mix?child_id={seed_family['child_id']}",
            headers={"Authorization": f"Bearer {family_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "korean_ratio" in data or "koreanRatio" in data

    async def test_insights_behavior(self, client, family_token, seed_family):
        """GET /v1/parent/insights/behavior → behavior patterns."""
        resp = await client.get(
            f"/v1/parent/insights/behavior?child_id={seed_family['child_id']}",
            headers={"Authorization": f"Bearer {family_token}"},
        )
        assert resp.status_code == 200

    async def test_parent_no_auth(self, client):
        """Parent endpoints without auth → 401."""
        resp = await client.get("/v1/parent/children")
        assert resp.status_code == 401

    async def test_parent_wrong_child(self, client, family_token):
        """Dashboard stats with wrong child_id → 403 or 404."""
        import uuid
        resp = await client.get(
            f"/v1/parent/dashboard/stats?child_id={uuid.uuid4()}",
            headers={"Authorization": f"Bearer {family_token}"},
        )
        assert resp.status_code in (403, 404)
