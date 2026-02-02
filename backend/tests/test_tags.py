"""Contract tests for tag-related API endpoints.

Tests are organized by User Story (US) following the tasks.md structure.
All tests follow TDD Red-Green-Refactor: write tests FIRST, ensure they FAIL,
then implement the feature.

Reference: specs/api/rest-endpoints.md, contracts/openapi.yaml
"""

import pytest
from fastapi.testclient import TestClient

from models import Tag, User


# =============================================================================
# User Story 8 (US8): Add Tags/Categories - Contract Tests
# =============================================================================


class TestTagListing:
    """Contract tests for GET /api/{user_id}/tags endpoint (T100)."""

    def test_list_tags_empty(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T100: List tags returns empty array when user has no tags.

        Contract:
        - GET /api/{user_id}/tags returns 200
        - Response contains empty tags array when no tags exist
        """
        response = client.get(
            f"/api/{test_user.id}/tags",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "tags" in data["data"]
        assert data["data"]["tags"] == []

    def test_list_tags_after_task_creation(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T100: Tags created via task creation are listed.

        Contract:
        - Tags created when adding to tasks appear in list
        - Tags are unique per user (no duplicates)
        """
        # Create tasks with tags
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task 1", "tags": ["work", "urgent"]},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task 2", "tags": ["work", "home"]},
            headers=auth_headers,
        )

        # List tags
        response = client.get(
            f"/api/{test_user.id}/tags",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        tags = data["data"]["tags"]

        # Should have 3 unique tags: work, urgent, home
        tag_names = [t["name"] for t in tags]
        assert set(tag_names) == {"work", "urgent", "home"}

    def test_list_tags_returns_tag_details(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T100: Listed tags contain id, name, and created_at fields."""
        # Create a task with tags
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Tagged task", "tags": ["project"]},
            headers=auth_headers,
        )

        # List tags
        response = client.get(
            f"/api/{test_user.id}/tags",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tags = response.json()["data"]["tags"]
        assert len(tags) == 1

        tag = tags[0]
        assert "id" in tag
        assert "name" in tag
        assert tag["name"] == "project"
        assert "created_at" in tag

    def test_list_tags_sorted_alphabetically(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T100: Tags are sorted alphabetically by name."""
        # Create tasks with tags in non-alphabetical order
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task", "tags": ["zebra", "alpha", "middle"]},
            headers=auth_headers,
        )

        # List tags
        response = client.get(
            f"/api/{test_user.id}/tags",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tags = response.json()["data"]["tags"]
        tag_names = [t["name"] for t in tags]

        # Should be alphabetically sorted
        assert tag_names == sorted(tag_names)


class TestTagListingUserIsolation:
    """Contract tests for tag user isolation (T100)."""

    def test_list_tags_user_isolation(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        auth_headers: dict[str, str],
        other_auth_headers: dict[str, str],
    ):
        """T100: Users can only see their own tags.

        Contract:
        - User A's tags are not visible to User B
        - Each user only sees tags they created
        """
        # Create tags for test_user
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "User 1 Task", "tags": ["user1-tag", "shared-name"]},
            headers=auth_headers,
        )

        # Create tags for other_user
        client.post(
            f"/api/{other_user.id}/tasks",
            json={"title": "User 2 Task", "tags": ["user2-tag", "shared-name"]},
            headers=other_auth_headers,
        )

        # test_user should only see their tags
        response = client.get(
            f"/api/{test_user.id}/tags",
            headers=auth_headers,
        )
        assert response.status_code == 200
        test_user_tags = [t["name"] for t in response.json()["data"]["tags"]]
        assert "user1-tag" in test_user_tags
        assert "shared-name" in test_user_tags
        assert "user2-tag" not in test_user_tags

        # other_user should only see their tags
        response = client.get(
            f"/api/{other_user.id}/tags",
            headers=other_auth_headers,
        )
        assert response.status_code == 200
        other_user_tags = [t["name"] for t in response.json()["data"]["tags"]]
        assert "user2-tag" in other_user_tags
        assert "shared-name" in other_user_tags
        assert "user1-tag" not in other_user_tags

    def test_list_tags_forbidden_other_user(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        auth_headers: dict[str, str],
    ):
        """T100: Return 403 when trying to list another user's tags."""
        response = client.get(
            f"/api/{other_user.id}/tags",
            headers=auth_headers,  # test_user's token
        )

        assert response.status_code == 403


class TestTagListingAuth:
    """Contract tests for tag endpoint authentication (T100)."""

    def test_list_tags_requires_auth(
        self,
        client: TestClient,
        test_user: User,
    ):
        """T100: Return 401 when no authorization header provided."""
        response = client.get(f"/api/{test_user.id}/tags")

        assert response.status_code == 401

    def test_list_tags_invalid_token(
        self,
        client: TestClient,
        test_user: User,
    ):
        """T100: Return 401 when token is invalid."""
        response = client.get(
            f"/api/{test_user.id}/tags",
            headers={"Authorization": "Bearer invalid-token"},
        )

        assert response.status_code == 401


# =============================================================================
# User Story 8 (US8): Tags in Task Creation/Update - Contract Tests
# =============================================================================


class TestTagsInTaskCreation:
    """Contract tests for tags in task creation (T101)."""

    def test_create_task_with_single_tag(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T101: Create task with a single tag."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Single tag task", "tags": ["work"]},
            headers=auth_headers,
        )

        assert response.status_code == 201
        assert response.json()["data"]["tags"] == ["work"]

    def test_create_task_with_multiple_tags(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T101: Create task with multiple tags."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Multi-tag task", "tags": ["work", "urgent", "project"]},
            headers=auth_headers,
        )

        assert response.status_code == 201
        assert set(response.json()["data"]["tags"]) == {"work", "urgent", "project"}

    def test_create_task_without_tags(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T101: Create task without tags defaults to empty array."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "No tags task"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        assert response.json()["data"]["tags"] == []

    def test_create_task_tags_normalized(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T101: Tags are normalized (lowercase, trimmed)."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Normalized tags", "tags": ["  WORK  ", "HOME"]},
            headers=auth_headers,
        )

        assert response.status_code == 201
        tags = response.json()["data"]["tags"]
        # Tags should be lowercase and trimmed
        assert set(tags) == {"work", "home"}

    def test_create_task_duplicate_tags_deduplicated(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T101: Duplicate tags in request are deduplicated."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Duplicate tags", "tags": ["work", "work", "WORK"]},
            headers=auth_headers,
        )

        assert response.status_code == 201
        tags = response.json()["data"]["tags"]
        # Should only have one "work" tag
        assert tags == ["work"]


class TestTagsInTaskUpdate:
    """Contract tests for tags in task update (T101)."""

    def test_update_task_add_tags(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T101: Add tags to existing task."""
        # Create task without tags
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task to tag"},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # Update to add tags
        update_response = client.put(
            f"/api/{test_user.id}/tasks/{task_id}",
            json={"tags": ["new-tag", "another"]},
            headers=auth_headers,
        )

        assert update_response.status_code == 200
        assert set(update_response.json()["data"]["tags"]) == {"new-tag", "another"}

    def test_update_task_replace_tags(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T101: Replace existing tags with new ones."""
        # Create task with tags
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task with tags", "tags": ["old1", "old2"]},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # Update to replace tags
        update_response = client.put(
            f"/api/{test_user.id}/tasks/{task_id}",
            json={"tags": ["new1", "new2"]},
            headers=auth_headers,
        )

        assert update_response.status_code == 200
        tags = update_response.json()["data"]["tags"]
        assert set(tags) == {"new1", "new2"}
        assert "old1" not in tags
        assert "old2" not in tags

    def test_update_task_clear_tags(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T101: Clear all tags from a task."""
        # Create task with tags
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task to clear tags", "tags": ["tag1", "tag2"]},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # Update to clear tags
        update_response = client.put(
            f"/api/{test_user.id}/tasks/{task_id}",
            json={"tags": []},
            headers=auth_headers,
        )

        assert update_response.status_code == 200
        assert update_response.json()["data"]["tags"] == []

    def test_update_task_tags_persisted(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T101: Updated tags are visible in task list."""
        # Create task
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Persistence test"},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # Update tags
        client.put(
            f"/api/{test_user.id}/tasks/{task_id}",
            json={"tags": ["persistent"]},
            headers=auth_headers,
        )

        # Verify in list
        list_response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )
        tasks = list_response.json()["data"]["tasks"]
        task = next((t for t in tasks if t["id"] == task_id), None)

        assert task is not None
        assert task["tags"] == ["persistent"]
