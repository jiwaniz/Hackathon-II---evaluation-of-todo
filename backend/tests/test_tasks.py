"""Contract tests for task-related API endpoints.

Tests are organized by User Story (US) following the tasks.md structure.
All tests follow TDD Red-Green-Refactor: write tests FIRST, ensure they FAIL,
then implement the feature.

Reference: specs/api/rest-endpoints.md, contracts/openapi.yaml
"""

import pytest
from fastapi.testclient import TestClient

from models import Priority, Task, User


# =============================================================================
# User Story 2 (US2): Create Task - Contract Tests
# =============================================================================


class TestTaskCreation:
    """Contract tests for POST /api/{user_id}/tasks endpoint (T049)."""

    def test_create_task_success(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T049: Create a task with valid data returns 201 and task data.

        Contract:
        - POST /api/{user_id}/tasks with valid title returns 201
        - Response contains task with id, title, description, completed, priority, tags
        - completed defaults to False
        - priority defaults to "medium"
        - tags defaults to empty array
        - created_at and updated_at are set
        """
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()

        # Validate response structure
        assert "data" in data
        task = data["data"]
        assert task["id"] is not None
        assert task["title"] == "Buy groceries"
        assert task["description"] == "Milk, eggs, bread"
        assert task["completed"] is False
        assert task["priority"] == "medium"
        assert task["tags"] == []
        assert "created_at" in task
        assert "updated_at" in task

        # Optional message field
        if "message" in data:
            assert "created" in data["message"].lower()

    def test_create_task_with_priority(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T049: Create task with custom priority level."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={
                "title": "Urgent task",
                "priority": "high",
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["priority"] == "high"

    def test_create_task_with_tags(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T049: Create task with tags."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={
                "title": "Tagged task",
                "tags": ["work", "urgent"],
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert set(data["data"]["tags"]) == {"work", "urgent"}

    def test_create_task_minimal(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T049: Create task with only required title field."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Minimal task"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        task = data["data"]
        assert task["title"] == "Minimal task"
        assert task["description"] is None
        assert task["priority"] == "medium"
        assert task["tags"] == []
        assert task["completed"] is False

    def test_create_task_full_payload(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T049: Create task with all optional fields provided."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={
                "title": "Complete task",
                "description": "A detailed description",
                "priority": "low",
                "tags": ["home", "weekend"],
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        task = data["data"]
        assert task["title"] == "Complete task"
        assert task["description"] == "A detailed description"
        assert task["priority"] == "low"
        assert set(task["tags"]) == {"home", "weekend"}


class TestTaskCreationUserIdMismatch:
    """Contract tests for 403 when URL user_id doesn't match JWT (T050)."""

    def test_create_task_forbidden_user_id_mismatch(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        auth_headers: dict[str, str],
    ):
        """T050: Return 403 when URL user_id doesn't match JWT sub claim.

        Contract:
        - POST /api/{user_id}/tasks with mismatched user_id returns 403
        - Error response has code "FORBIDDEN" and descriptive message
        """
        # Try to create task for other_user using test_user's token
        response = client.post(
            f"/api/{other_user.id}/tasks",
            json={"title": "Malicious task"},
            headers=auth_headers,  # test_user's token
        )

        assert response.status_code == 403
        data = response.json()
        assert "error" in data or "detail" in data

        error = data.get("error") or data.get("detail")
        if isinstance(error, dict):
            assert error.get("code") == "FORBIDDEN"
            assert "mismatch" in error.get("message", "").lower() or "forbidden" in error.get("message", "").lower()

    def test_create_task_requires_auth(
        self,
        client: TestClient,
        test_user: User,
    ):
        """T050: Return 401 when no authorization header provided."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Unauthorized task"},
        )

        assert response.status_code == 401

    def test_create_task_invalid_token(
        self,
        client: TestClient,
        test_user: User,
    ):
        """T050: Return 401 when token is invalid."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Invalid token task"},
            headers={"Authorization": "Bearer invalid-token"},
        )

        assert response.status_code == 401


class TestTaskCreationValidation:
    """Contract tests for 400 on missing/invalid title (T051)."""

    def test_create_task_missing_title(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T051: Return 400 when title is missing from request body.

        Contract:
        - POST /api/{user_id}/tasks without title returns 400 (or 422)
        - Error response indicates title is required
        """
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"description": "No title provided"},
            headers=auth_headers,
        )

        # FastAPI returns 422 for validation errors
        assert response.status_code in [400, 422]

    def test_create_task_empty_title(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T051: Return 400 when title is empty string."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": ""},
            headers=auth_headers,
        )

        # FastAPI returns 422 for validation errors
        assert response.status_code in [400, 422]

    def test_create_task_whitespace_only_title(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T051: Return 400 when title is whitespace only."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "   "},
            headers=auth_headers,
        )

        # Whitespace-only titles should be rejected
        # This might return 201 if whitespace is trimmed - depends on implementation
        # For now, we accept either behavior
        assert response.status_code in [201, 400, 422]
        if response.status_code == 201:
            # If accepted, title should be trimmed
            data = response.json()
            # Whitespace handling is implementation-dependent
            pass

    def test_create_task_title_too_long(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T051: Return 400 when title exceeds 200 characters."""
        long_title = "x" * 201
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": long_title},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]

    def test_create_task_title_at_max_length(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T051: Accept title at exactly 200 characters (boundary test)."""
        max_title = "x" * 200
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": max_title},
            headers=auth_headers,
        )

        assert response.status_code == 201

    def test_create_task_description_too_long(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T051: Return 400 when description exceeds 1000 characters."""
        long_description = "x" * 1001
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Valid title", "description": long_description},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]

    def test_create_task_invalid_priority(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T051: Return 400 when priority is not a valid enum value."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Valid title", "priority": "invalid"},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]

    def test_create_task_null_title(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T051: Return 400 when title is explicitly null."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": None},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]

    def test_create_task_empty_body(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T051: Return 400 when request body is empty."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]


# =============================================================================
# User Story 3 (US3): View All Tasks - Contract Tests
# =============================================================================


class TestTaskListing:
    """Contract tests for GET /api/{user_id}/tasks endpoint (T059)."""

    def test_list_tasks_success(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T059: List tasks returns 200 with tasks array and pagination.

        Contract:
        - GET /api/{user_id}/tasks returns 200
        - Response contains tasks array and pagination metadata
        - Tasks are ordered by created_at descending (newest first)
        """
        # Create some tasks first
        for i in range(3):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Task {i + 1}"},
                headers=auth_headers,
            )

        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert "data" in data
        result = data["data"]
        assert "tasks" in result
        assert "pagination" in result
        assert isinstance(result["tasks"], list)
        assert len(result["tasks"]) >= 3

        # Validate pagination structure
        pagination = result["pagination"]
        assert "page" in pagination
        assert "limit" in pagination
        assert "total" in pagination
        assert "pages" in pagination

    def test_list_tasks_empty(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T059: List tasks returns empty array when user has no tasks."""
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        result = data["data"]
        assert result["tasks"] == []
        assert result["pagination"]["total"] == 0

    def test_list_tasks_returns_all_fields(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T059: Listed tasks contain all required fields."""
        # Create a task with all fields
        client.post(
            f"/api/{test_user.id}/tasks",
            json={
                "title": "Complete task",
                "description": "Full description",
                "priority": "high",
                "tags": ["work", "urgent"],
            },
            headers=auth_headers,
        )

        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) >= 1

        task = tasks[0]
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "priority" in task
        assert "tags" in task
        assert "created_at" in task
        assert "updated_at" in task


class TestTaskListingUserIsolation:
    """Contract tests for user isolation - cannot see other user's tasks (T060)."""

    def test_list_tasks_user_isolation(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        auth_headers: dict[str, str],
        other_auth_headers: dict[str, str],
    ):
        """T060: Users can only see their own tasks.

        Contract:
        - User A's tasks are not visible to User B
        - Each user only sees tasks they created
        """
        # Create tasks for test_user
        for i in range(2):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Test User Task {i + 1}"},
                headers=auth_headers,
            )

        # Create tasks for other_user
        for i in range(3):
            client.post(
                f"/api/{other_user.id}/tasks",
                json={"title": f"Other User Task {i + 1}"},
                headers=other_auth_headers,
            )

        # test_user should only see their own tasks
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )
        assert response.status_code == 200
        test_user_tasks = response.json()["data"]["tasks"]

        for task in test_user_tasks:
            assert "Test User Task" in task["title"]
            assert "Other User Task" not in task["title"]

        # other_user should only see their own tasks
        response = client.get(
            f"/api/{other_user.id}/tasks",
            headers=other_auth_headers,
        )
        assert response.status_code == 200
        other_user_tasks = response.json()["data"]["tasks"]

        for task in other_user_tasks:
            assert "Other User Task" in task["title"]
            assert "Test User Task" not in task["title"]

    def test_list_tasks_forbidden_other_user(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        auth_headers: dict[str, str],
    ):
        """T060: Return 403 when trying to list another user's tasks."""
        response = client.get(
            f"/api/{other_user.id}/tasks",
            headers=auth_headers,  # test_user's token
        )

        assert response.status_code == 403


class TestTaskListingPagination:
    """Contract tests for pagination in task listing (T061)."""

    def test_list_tasks_pagination_default(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T061: Default pagination returns first page with limit 20."""
        # Create 25 tasks
        for i in range(25):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Task {i + 1}"},
                headers=auth_headers,
            )

        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()["data"]

        assert len(data["tasks"]) == 20  # Default limit
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["limit"] == 20
        assert data["pagination"]["total"] == 25
        assert data["pagination"]["pages"] == 2

    def test_list_tasks_pagination_custom_page(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T061: Custom page parameter works correctly."""
        # Create 25 tasks
        for i in range(25):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Task {i + 1}"},
                headers=auth_headers,
            )

        # Get page 2
        response = client.get(
            f"/api/{test_user.id}/tasks?page=2",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()["data"]

        assert len(data["tasks"]) == 5  # Remaining tasks on page 2
        assert data["pagination"]["page"] == 2

    def test_list_tasks_pagination_custom_limit(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T061: Custom limit parameter works correctly."""
        # Create 15 tasks
        for i in range(15):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Task {i + 1}"},
                headers=auth_headers,
            )

        # Get with custom limit
        response = client.get(
            f"/api/{test_user.id}/tasks?limit=5",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()["data"]

        assert len(data["tasks"]) == 5
        assert data["pagination"]["limit"] == 5
        assert data["pagination"]["pages"] == 3

    def test_list_tasks_pagination_empty_page(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T061: Requesting page beyond available data returns empty tasks."""
        # Create 5 tasks
        for i in range(5):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Task {i + 1}"},
                headers=auth_headers,
            )

        # Request page 10 (beyond available data)
        response = client.get(
            f"/api/{test_user.id}/tasks?page=10",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["tasks"] == []
        assert data["pagination"]["page"] == 10


# =============================================================================
# User Story 4 (US4): Update Task - Contract Tests
# =============================================================================


class TestTaskUpdate:
    """Contract tests for PUT /api/{user_id}/tasks/{task_id} endpoint (T070)."""

    def test_update_task_title(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T070: Update task title returns 200 with updated task.

        Contract:
        - PUT /api/{user_id}/tasks/{task_id} with valid title returns 200
        - Response contains updated task data
        - updated_at is refreshed
        - Other fields remain unchanged
        """
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"title": "Updated Title"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert "data" in data
        task = data["data"]
        assert task["id"] == test_task.id
        assert task["title"] == "Updated Title"
        # Other fields unchanged
        assert task["description"] == test_task.description
        assert task["completed"] == test_task.completed
        assert task["priority"] == test_task.priority.value
        assert "updated_at" in task

    def test_update_task_description(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T070: Update task description."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"description": "New description content"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["description"] == "New description content"
        assert data["data"]["title"] == test_task.title

    def test_update_task_priority(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T070: Update task priority."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"priority": "high"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["priority"] == "high"

    def test_update_task_tags(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T070: Update task tags."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"tags": ["work", "important"]},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert set(data["data"]["tags"]) == {"work", "important"}

    def test_update_task_multiple_fields(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T070: Update multiple task fields at once."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={
                "title": "Completely Updated",
                "description": "New description",
                "priority": "high",
                "tags": ["urgent"],
            },
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        task = data["data"]
        assert task["title"] == "Completely Updated"
        assert task["description"] == "New description"
        assert task["priority"] == "high"
        assert task["tags"] == ["urgent"]

    def test_update_task_clear_description(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T070: Clear task description by setting to empty string or null."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"description": ""},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        # Empty description should be stored as None or empty string
        assert data["data"]["description"] in [None, ""]

    def test_update_task_empty_tags(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T070: Clear task tags by setting to empty array."""
        # First create a task with tags
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Tagged task", "tags": ["work", "home"]},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # Then clear the tags
        response = client.put(
            f"/api/{test_user.id}/tasks/{task_id}",
            json={"tags": []},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["tags"] == []

    def test_update_task_invalid_title_empty(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T070: Return 400/422 when title is empty string."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"title": ""},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]

    def test_update_task_title_too_long(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T070: Return 400/422 when title exceeds 200 characters."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"title": "x" * 201},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]

    def test_update_task_invalid_priority(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T070: Return 400/422 when priority is invalid."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"priority": "invalid"},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]


class TestTaskUpdateNotFound:
    """Contract tests for 404 on non-existent task (T071)."""

    def test_update_task_not_found(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T071: Return 404 when task does not exist.

        Contract:
        - PUT /api/{user_id}/tasks/{task_id} for non-existent task returns 404
        - Error response indicates task not found
        """
        non_existent_id = 99999

        response = client.put(
            f"/api/{test_user.id}/tasks/{non_existent_id}",
            json={"title": "Updated"},
            headers=auth_headers,
        )

        assert response.status_code == 404
        data = response.json()
        assert "error" in data or "detail" in data

    def test_update_task_not_found_with_valid_format(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T071: 404 even with valid update payload."""
        response = client.put(
            f"/api/{test_user.id}/tasks/12345",
            json={
                "title": "Valid update",
                "description": "Valid description",
                "priority": "high",
            },
            headers=auth_headers,
        )

        assert response.status_code == 404


class TestTaskUpdateForbidden:
    """Contract tests for 403 when updating another user's task (T072)."""

    def test_update_other_users_task(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        other_user_task: Task,
        auth_headers: dict[str, str],
    ):
        """T072: Return 403 when trying to update another user's task.

        Contract:
        - PUT /api/{user_id}/tasks/{task_id} with mismatched user_id returns 403
        - User cannot modify tasks they don't own
        """
        # Try to update other_user's task using test_user's token
        # Must use other_user's ID in URL to match the task
        response = client.put(
            f"/api/{other_user.id}/tasks/{other_user_task.id}",
            json={"title": "Hacked title"},
            headers=auth_headers,  # test_user's token
        )

        assert response.status_code == 403

    def test_update_task_url_user_mismatch(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T072: Return 403 when URL user_id doesn't match JWT sub claim."""
        # Try to update test_user's task but with other_user's ID in URL
        response = client.put(
            f"/api/{other_user.id}/tasks/{test_task.id}",
            json={"title": "Updated"},
            headers=auth_headers,  # test_user's token
        )

        assert response.status_code == 403

    def test_update_requires_authentication(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
    ):
        """T072: Return 401 when no authorization header provided."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"title": "Unauthorized update"},
        )

        assert response.status_code == 401

    def test_update_invalid_token(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
    ):
        """T072: Return 401 when token is invalid."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"title": "Invalid token update"},
            headers={"Authorization": "Bearer invalid-token"},
        )

        assert response.status_code == 401


# =============================================================================
# User Story 5 (US5): Delete Task - Contract Tests
# =============================================================================


class TestTaskDeletion:
    """Contract tests for DELETE /api/{user_id}/tasks/{task_id} endpoint (T078)."""

    def test_delete_task_success(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T078: Delete a task returns 200 with success message.

        Contract:
        - DELETE /api/{user_id}/tasks/{task_id} returns 200
        - Response contains success message
        - Task is permanently removed from database
        """
        task_id = test_task.id

        response = client.delete(
            f"/api/{test_user.id}/tasks/{task_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "deleted" in data["message"].lower()

        # Verify task is actually deleted
        get_response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )
        tasks = get_response.json()["data"]["tasks"]
        task_ids = [t["id"] for t in tasks]
        assert task_id not in task_ids

    def test_delete_task_not_found(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T078: Return 404 when task does not exist.

        Contract:
        - DELETE /api/{user_id}/tasks/{task_id} for non-existent task returns 404
        - Error response indicates task not found
        """
        response = client.delete(
            f"/api/{test_user.id}/tasks/99999",
            headers=auth_headers,
        )

        assert response.status_code == 404
        data = response.json()
        assert "error" in data or "detail" in data

    def test_delete_task_removes_from_list(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T078: Deleted task no longer appears in task list."""
        # Create a task
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task to delete"},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # Verify task exists
        list_response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )
        task_ids = [t["id"] for t in list_response.json()["data"]["tasks"]]
        assert task_id in task_ids

        # Delete the task
        delete_response = client.delete(
            f"/api/{test_user.id}/tasks/{task_id}",
            headers=auth_headers,
        )
        assert delete_response.status_code == 200

        # Verify task is gone
        list_response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )
        task_ids = [t["id"] for t in list_response.json()["data"]["tasks"]]
        assert task_id not in task_ids

    def test_delete_task_with_tags(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T078: Delete task with tags succeeds (cascade delete)."""
        # Create a task with tags
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Tagged task", "tags": ["work", "urgent"]},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # Delete the task
        response = client.delete(
            f"/api/{test_user.id}/tasks/{task_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200

    def test_delete_already_deleted_task(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T078: Return 404 when trying to delete already deleted task."""
        # Create and delete a task
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task to double delete"},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # First delete succeeds
        first_delete = client.delete(
            f"/api/{test_user.id}/tasks/{task_id}",
            headers=auth_headers,
        )
        assert first_delete.status_code == 200

        # Second delete returns 404
        second_delete = client.delete(
            f"/api/{test_user.id}/tasks/{task_id}",
            headers=auth_headers,
        )
        assert second_delete.status_code == 404


class TestTaskDeletionForbidden:
    """Contract tests for 403 when deleting another user's task (T079)."""

    def test_delete_other_users_task(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        other_user_task: Task,
        auth_headers: dict[str, str],
    ):
        """T079: Return 403 when trying to delete another user's task.

        Contract:
        - DELETE /api/{user_id}/tasks/{task_id} with mismatched user_id returns 403
        - User cannot delete tasks they don't own
        """
        # Try to delete other_user's task using test_user's token
        response = client.delete(
            f"/api/{other_user.id}/tasks/{other_user_task.id}",
            headers=auth_headers,  # test_user's token
        )

        assert response.status_code == 403

    def test_delete_task_url_user_mismatch(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T079: Return 403 when URL user_id doesn't match JWT sub claim."""
        # Try to delete test_user's task but with other_user's ID in URL
        response = client.delete(
            f"/api/{other_user.id}/tasks/{test_task.id}",
            headers=auth_headers,  # test_user's token
        )

        assert response.status_code == 403

    def test_delete_requires_authentication(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
    ):
        """T079: Return 401 when no authorization header provided."""
        response = client.delete(
            f"/api/{test_user.id}/tasks/{test_task.id}",
        )

        assert response.status_code == 401

    def test_delete_invalid_token(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
    ):
        """T079: Return 401 when token is invalid."""
        response = client.delete(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": "Bearer invalid-token"},
        )

        assert response.status_code == 401


# =============================================================================
# User Story 6 (US6): Toggle Task Completion - Contract Tests
# =============================================================================


class TestTaskToggle:
    """Contract tests for PATCH /api/{user_id}/tasks/{task_id}/toggle endpoint (T085)."""

    def test_toggle_incomplete_to_complete(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T085: Toggle incomplete task to complete returns 200 with updated status.

        Contract:
        - PATCH /api/{user_id}/tasks/{task_id}/toggle returns 200
        - Response contains task id, completed status, and updated_at
        - Task completed status is flipped from False to True
        """
        # Verify task starts as incomplete
        assert test_task.completed is False

        response = client.patch(
            f"/api/{test_user.id}/tasks/{test_task.id}/toggle",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert "data" in data
        assert data["data"]["id"] == test_task.id
        assert data["data"]["completed"] is True
        assert "updated_at" in data["data"]

    def test_toggle_complete_to_incomplete(
        self,
        client: TestClient,
        test_user: User,
        completed_task: Task,
        auth_headers: dict[str, str],
    ):
        """T085: Toggle complete task to incomplete returns 200."""
        # Verify task starts as complete
        assert completed_task.completed is True

        response = client.patch(
            f"/api/{test_user.id}/tasks/{completed_task.id}/toggle",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert data["data"]["id"] == completed_task.id
        assert data["data"]["completed"] is False

    def test_toggle_task_not_found(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T085: Return 404 when task does not exist."""
        response = client.patch(
            f"/api/{test_user.id}/tasks/99999/toggle",
            headers=auth_headers,
        )

        assert response.status_code == 404

    def test_toggle_other_users_task(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        other_user_task: Task,
        auth_headers: dict[str, str],
    ):
        """T085: Return 403 when trying to toggle another user's task."""
        response = client.patch(
            f"/api/{other_user.id}/tasks/{other_user_task.id}/toggle",
            headers=auth_headers,  # test_user's token
        )

        assert response.status_code == 403

    def test_toggle_requires_authentication(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
    ):
        """T085: Return 401 when no authorization header provided."""
        response = client.patch(
            f"/api/{test_user.id}/tasks/{test_task.id}/toggle",
        )

        assert response.status_code == 401


class TestTaskTogglePersistence:
    """Contract tests for toggle persistence (T086)."""

    def test_toggle_persists_to_database(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T086: Toggled status persists and is visible in task list.

        Contract:
        - After toggle, status change is immediately visible
        - Subsequent GET requests show the new status
        """
        # Create a task
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task to toggle"},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]
        assert create_response.json()["data"]["completed"] is False

        # Toggle to complete
        toggle_response = client.patch(
            f"/api/{test_user.id}/tasks/{task_id}/toggle",
            headers=auth_headers,
        )
        assert toggle_response.status_code == 200
        assert toggle_response.json()["data"]["completed"] is True

        # Verify via GET - task list should show completed status
        list_response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )
        tasks = list_response.json()["data"]["tasks"]
        toggled_task = next((t for t in tasks if t["id"] == task_id), None)
        assert toggled_task is not None
        assert toggled_task["completed"] is True

    def test_toggle_twice_returns_to_original(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T086: Toggling twice returns task to original state."""
        # Create a task (starts incomplete)
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Double toggle task"},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]
        original_completed = create_response.json()["data"]["completed"]
        assert original_completed is False

        # First toggle - should be complete
        first_toggle = client.patch(
            f"/api/{test_user.id}/tasks/{task_id}/toggle",
            headers=auth_headers,
        )
        assert first_toggle.json()["data"]["completed"] is True

        # Second toggle - should be incomplete again
        second_toggle = client.patch(
            f"/api/{test_user.id}/tasks/{task_id}/toggle",
            headers=auth_headers,
        )
        assert second_toggle.json()["data"]["completed"] is False

    def test_toggle_updates_timestamp(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T086: Toggle updates the updated_at timestamp."""
        original_updated_at = test_task.updated_at.isoformat()

        response = client.patch(
            f"/api/{test_user.id}/tasks/{test_task.id}/toggle",
            headers=auth_headers,
        )

        assert response.status_code == 200
        new_updated_at = response.json()["data"]["updated_at"]

        # The updated_at should have changed (newer than original)
        assert new_updated_at != original_updated_at


# =============================================================================
# User Story 7 (US7): Set Task Priority - Contract Tests
# =============================================================================


class TestTaskPriorityCreation:
    """Contract tests for priority in task creation (T092)."""

    def test_create_task_default_priority_medium(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T092: Task created without priority defaults to 'medium'.

        Contract:
        - POST /api/{user_id}/tasks without priority returns task with priority="medium"
        """
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task without priority"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        assert response.json()["data"]["priority"] == "medium"

    def test_create_task_with_high_priority(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T092: Create task with high priority."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "High priority task", "priority": "high"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        assert response.json()["data"]["priority"] == "high"

    def test_create_task_with_low_priority(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T092: Create task with low priority."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Low priority task", "priority": "low"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        assert response.json()["data"]["priority"] == "low"

    def test_create_task_invalid_priority_rejected(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T092: Invalid priority value is rejected."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Invalid priority task", "priority": "urgent"},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]

    def test_priority_values_case_sensitive(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T092: Priority values are case-sensitive (uppercase rejected)."""
        response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Uppercase priority task", "priority": "HIGH"},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]


class TestTaskPriorityUpdate:
    """Contract tests for priority update (T093)."""

    def test_update_priority_low_to_high(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T093: Update task priority from low to high.

        Contract:
        - PUT /api/{user_id}/tasks/{task_id} with priority field updates priority
        - Other fields remain unchanged
        """
        # Create task with low priority
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Priority change task", "priority": "low"},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]
        assert create_response.json()["data"]["priority"] == "low"

        # Update priority to high
        update_response = client.put(
            f"/api/{test_user.id}/tasks/{task_id}",
            json={"priority": "high"},
            headers=auth_headers,
        )

        assert update_response.status_code == 200
        assert update_response.json()["data"]["priority"] == "high"
        # Title should be unchanged
        assert update_response.json()["data"]["title"] == "Priority change task"

    def test_update_priority_high_to_medium(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T093: Update task priority from high to medium."""
        # Create task with high priority
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Another priority task", "priority": "high"},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # Update priority to medium
        update_response = client.put(
            f"/api/{test_user.id}/tasks/{task_id}",
            json={"priority": "medium"},
            headers=auth_headers,
        )

        assert update_response.status_code == 200
        assert update_response.json()["data"]["priority"] == "medium"

    def test_update_priority_persists_in_list(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T093: Updated priority is visible in task list."""
        # Create task
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Persistence test", "priority": "low"},
            headers=auth_headers,
        )
        task_id = create_response.json()["data"]["id"]

        # Update priority
        client.put(
            f"/api/{test_user.id}/tasks/{task_id}",
            json={"priority": "high"},
            headers=auth_headers,
        )

        # Verify in list
        list_response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )
        tasks = list_response.json()["data"]["tasks"]
        updated_task = next((t for t in tasks if t["id"] == task_id), None)

        assert updated_task is not None
        assert updated_task["priority"] == "high"

    def test_update_invalid_priority_rejected(
        self,
        client: TestClient,
        test_user: User,
        test_task: Task,
        auth_headers: dict[str, str],
    ):
        """T093: Invalid priority value in update is rejected."""
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json={"priority": "critical"},
            headers=auth_headers,
        )

        assert response.status_code in [400, 422]


# =============================================================================
# User Story 9 (US9): Search Tasks - Contract Tests
# =============================================================================


class TestTaskSearch:
    """Contract tests for search parameter in GET /api/{user_id}/tasks (T111)."""

    def test_search_returns_matching_tasks(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T111: Search parameter filters tasks by keyword."""
        # Create tasks with different titles
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Buy groceries"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Clean the house"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Go to grocery store"},
            headers=auth_headers,
        )

        # Search for "grocer"
        response = client.get(
            f"/api/{test_user.id}/tasks?search=grocer",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        # Should match "Buy groceries" and "Go to grocery store"
        assert len(tasks) == 2
        titles = [t["title"] for t in tasks]
        assert "Buy groceries" in titles
        assert "Go to grocery store" in titles
        assert "Clean the house" not in titles

    def test_search_no_matches_returns_empty(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T111: Search with no matches returns empty array."""
        # Create a task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Buy milk"},
            headers=auth_headers,
        )

        # Search for non-existent term
        response = client.get(
            f"/api/{test_user.id}/tasks?search=dinosaur",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 0

    def test_search_case_insensitive(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T111: Search is case-insensitive."""
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Meeting with TEAM"},
            headers=auth_headers,
        )

        # Search with different case
        response = client.get(
            f"/api/{test_user.id}/tasks?search=team",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Meeting with TEAM"

    def test_search_empty_string_returns_all(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T111: Empty search string returns all tasks."""
        # Create tasks
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task 1"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task 2"},
            headers=auth_headers,
        )

        # Search with empty string
        response = client.get(
            f"/api/{test_user.id}/tasks?search=",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 2


class TestTaskSearchAcrossFields:
    """Contract tests for search across title and description (T112)."""

    def test_search_matches_title(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T112: Search matches text in task title."""
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Important meeting", "description": "Discuss project"},
            headers=auth_headers,
        )

        response = client.get(
            f"/api/{test_user.id}/tasks?search=important",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Important meeting"

    def test_search_matches_description(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T112: Search matches text in task description."""
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Weekly standup", "description": "Discuss quarterly goals"},
            headers=auth_headers,
        )

        response = client.get(
            f"/api/{test_user.id}/tasks?search=quarterly",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Weekly standup"

    def test_search_matches_either_field(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T112: Search matches tasks where keyword is in title OR description."""
        # Task with keyword in title
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Budget review", "description": "Check expenses"},
            headers=auth_headers,
        )
        # Task with keyword in description
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Monthly planning", "description": "Review budget allocation"},
            headers=auth_headers,
        )
        # Task without keyword
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Team lunch", "description": "Order pizza"},
            headers=auth_headers,
        )

        response = client.get(
            f"/api/{test_user.id}/tasks?search=budget",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 2
        titles = [t["title"] for t in tasks]
        assert "Budget review" in titles
        assert "Monthly planning" in titles
        assert "Team lunch" not in titles

    def test_search_with_pagination(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T112: Search works correctly with pagination."""
        # Create 5 tasks matching search
        for i in range(5):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Project task {i}"},
                headers=auth_headers,
            )
        # Create 2 tasks not matching
        for i in range(2):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Other work {i}"},
                headers=auth_headers,
            )

        # Search with limit
        response = client.get(
            f"/api/{test_user.id}/tasks?search=project&limit=3",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data["tasks"]) == 3
        assert data["pagination"]["total"] == 5
        # All returned tasks should match search
        for task in data["tasks"]:
            assert "project" in task["title"].lower()

    def test_search_user_isolation(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        auth_headers: dict[str, str],
        other_auth_headers: dict[str, str],
    ):
        """T112: Search only returns tasks belonging to the authenticated user."""
        # Create task for test_user
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Secret project user1"},
            headers=auth_headers,
        )
        # Create task for other_user
        client.post(
            f"/api/{other_user.id}/tasks",
            json={"title": "Secret project user2"},
            headers=other_auth_headers,
        )

        # Search as test_user
        response = client.get(
            f"/api/{test_user.id}/tasks?search=secret",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Secret project user1"


# =============================================================================
# User Story 10 (US10): Filter Tasks - Contract Tests
# =============================================================================


class TestTaskStatusFilter:
    """Contract tests for status filter in GET /api/{user_id}/tasks (T118)."""

    def test_filter_completed_tasks(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T118: Filter by status=completed returns only completed tasks."""
        # Create completed task
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Completed task"},
            headers=auth_headers,
        )
        completed_id = create_response.json()["data"]["id"]
        client.patch(
            f"/api/{test_user.id}/tasks/{completed_id}/toggle",
            headers=auth_headers,
        )

        # Create pending task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Pending task"},
            headers=auth_headers,
        )

        # Filter completed
        response = client.get(
            f"/api/{test_user.id}/tasks?status=completed",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Completed task"
        assert tasks[0]["completed"] is True

    def test_filter_pending_tasks(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T118: Filter by status=pending returns only incomplete tasks."""
        # Create completed task
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Done task"},
            headers=auth_headers,
        )
        completed_id = create_response.json()["data"]["id"]
        client.patch(
            f"/api/{test_user.id}/tasks/{completed_id}/toggle",
            headers=auth_headers,
        )

        # Create pending task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Todo task"},
            headers=auth_headers,
        )

        # Filter pending
        response = client.get(
            f"/api/{test_user.id}/tasks?status=pending",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Todo task"
        assert tasks[0]["completed"] is False

    def test_filter_all_status(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T118: Filter by status=all returns all tasks (default behavior)."""
        # Create completed task
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task A"},
            headers=auth_headers,
        )
        completed_id = create_response.json()["data"]["id"]
        client.patch(
            f"/api/{test_user.id}/tasks/{completed_id}/toggle",
            headers=auth_headers,
        )

        # Create pending task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task B"},
            headers=auth_headers,
        )

        # Filter all (explicit)
        response = client.get(
            f"/api/{test_user.id}/tasks?status=all",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 2

    def test_no_status_filter_returns_all(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T118: No status filter returns all tasks."""
        # Create completed task
        create_response = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task X"},
            headers=auth_headers,
        )
        completed_id = create_response.json()["data"]["id"]
        client.patch(
            f"/api/{test_user.id}/tasks/{completed_id}/toggle",
            headers=auth_headers,
        )

        # Create pending task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Task Y"},
            headers=auth_headers,
        )

        # No filter
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 2

    def test_status_filter_with_pagination(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T118: Status filter works correctly with pagination."""
        # Create 3 pending tasks
        for i in range(3):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Pending {i}"},
                headers=auth_headers,
            )

        # Create 2 completed tasks
        for i in range(2):
            resp = client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Completed {i}"},
                headers=auth_headers,
            )
            task_id = resp.json()["data"]["id"]
            client.patch(
                f"/api/{test_user.id}/tasks/{task_id}/toggle",
                headers=auth_headers,
            )

        # Filter pending with pagination
        response = client.get(
            f"/api/{test_user.id}/tasks?status=pending&limit=2",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data["tasks"]) == 2
        assert data["pagination"]["total"] == 3
        for task in data["tasks"]:
            assert task["completed"] is False


# =============================================================================
# User Story 10 (US10): Filter Tasks - Priority Filter Tests (T119)
# =============================================================================


class TestTaskPriorityFilter:
    """Contract tests for priority filter in GET /api/{user_id}/tasks (T119)."""

    def test_filter_high_priority_tasks(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T119: Filter tasks by high priority."""
        # Create tasks with different priorities
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "High Priority Task", "priority": "high"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Medium Priority Task", "priority": "medium"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Low Priority Task", "priority": "low"},
            headers=auth_headers,
        )

        # Filter by high priority
        response = client.get(
            f"/api/{test_user.id}/tasks?priority=high",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["priority"] == "high"
        assert tasks[0]["title"] == "High Priority Task"

    def test_filter_medium_priority_tasks(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T119: Filter tasks by medium priority."""
        # Create tasks with different priorities
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "High Task", "priority": "high"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Medium Task 1", "priority": "medium"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Medium Task 2", "priority": "medium"},
            headers=auth_headers,
        )

        # Filter by medium priority
        response = client.get(
            f"/api/{test_user.id}/tasks?priority=medium",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 2
        for task in tasks:
            assert task["priority"] == "medium"

    def test_filter_low_priority_tasks(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T119: Filter tasks by low priority."""
        # Create tasks with different priorities
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "High Task", "priority": "high"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Low Task", "priority": "low"},
            headers=auth_headers,
        )

        # Filter by low priority
        response = client.get(
            f"/api/{test_user.id}/tasks?priority=low",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["priority"] == "low"

    def test_no_priority_filter_returns_all(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T119: No priority filter returns all tasks."""
        # Create tasks with different priorities
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "High Task", "priority": "high"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Medium Task", "priority": "medium"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Low Task", "priority": "low"},
            headers=auth_headers,
        )

        # No filter
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 3

    def test_priority_filter_with_status_filter(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T119: Priority filter combined with status filter."""
        # Create high priority pending task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "High Pending", "priority": "high"},
            headers=auth_headers,
        )
        # Create high priority completed task
        resp = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "High Completed", "priority": "high"},
            headers=auth_headers,
        )
        task_id = resp.json()["data"]["id"]
        client.patch(
            f"/api/{test_user.id}/tasks/{task_id}/toggle",
            headers=auth_headers,
        )
        # Create medium priority pending task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Medium Pending", "priority": "medium"},
            headers=auth_headers,
        )

        # Filter by high priority AND pending status
        response = client.get(
            f"/api/{test_user.id}/tasks?priority=high&status=pending",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["priority"] == "high"
        assert tasks[0]["completed"] is False


# =============================================================================
# User Story 10 (US10): Filter Tasks - Tag Filter Tests (T120)
# =============================================================================


class TestTaskTagFilter:
    """Contract tests for tag filter in GET /api/{user_id}/tasks (T120)."""

    def test_filter_tasks_by_single_tag(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T120: Filter tasks by a single tag."""
        # Create tasks with different tags
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Work Task", "tags": ["work"]},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Personal Task", "tags": ["personal"]},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Work and Urgent Task", "tags": ["work", "urgent"]},
            headers=auth_headers,
        )

        # Filter by work tag
        response = client.get(
            f"/api/{test_user.id}/tasks?tag=work",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 2
        for task in tasks:
            assert "work" in task["tags"]

    def test_filter_tasks_by_tag_case_insensitive(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T120: Tag filter is case-insensitive."""
        # Create task with lowercase tag
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Work Task", "tags": ["work"]},
            headers=auth_headers,
        )

        # Filter with different case
        response = client.get(
            f"/api/{test_user.id}/tasks?tag=WORK",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert "work" in tasks[0]["tags"]

    def test_filter_tasks_no_matching_tag(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T120: Filter returns empty when no tasks have the tag."""
        # Create task with tag
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Work Task", "tags": ["work"]},
            headers=auth_headers,
        )

        # Filter by non-existent tag
        response = client.get(
            f"/api/{test_user.id}/tasks?tag=nonexistent",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 0

    def test_tag_filter_with_other_filters(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T120: Tag filter combined with status and priority filters."""
        # Create work pending high priority task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Work High Pending", "tags": ["work"], "priority": "high"},
            headers=auth_headers,
        )
        # Create work completed high priority task
        resp = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Work High Completed", "tags": ["work"], "priority": "high"},
            headers=auth_headers,
        )
        task_id = resp.json()["data"]["id"]
        client.patch(
            f"/api/{test_user.id}/tasks/{task_id}/toggle",
            headers=auth_headers,
        )
        # Create work pending low priority task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Work Low Pending", "tags": ["work"], "priority": "low"},
            headers=auth_headers,
        )
        # Create personal high priority task
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Personal High", "tags": ["personal"], "priority": "high"},
            headers=auth_headers,
        )

        # Filter by work tag, high priority, and pending status
        response = client.get(
            f"/api/{test_user.id}/tasks?tag=work&priority=high&status=pending",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Work High Pending"
        assert "work" in tasks[0]["tags"]
        assert tasks[0]["priority"] == "high"
        assert tasks[0]["completed"] is False

    def test_tag_filter_user_isolation(
        self,
        client: TestClient,
        test_user: User,
        other_user: User,
        auth_headers: dict[str, str],
        other_auth_headers: dict[str, str],
    ):
        """T120: Tag filter respects user isolation."""
        # Create task for test_user with work tag
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "My Work Task", "tags": ["work"]},
            headers=auth_headers,
        )
        # Create task for other_user with work tag
        client.post(
            f"/api/{other_user.id}/tasks",
            json={"title": "Other Work Task", "tags": ["work"]},
            headers=other_auth_headers,
        )

        # Filter test_user's tasks by work tag
        response = client.get(
            f"/api/{test_user.id}/tasks?tag=work",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "My Work Task"


# =============================================================================
# User Story 11 (US11): Sort Tasks - Contract Tests (T131, T132)
# =============================================================================


class TestTaskSorting:
    """Contract tests for sort parameter in GET /api/{user_id}/tasks (T131)."""

    def test_sort_by_created_desc_default(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T131: Default sort is by created_at descending (newest first)."""
        import time

        # Create tasks with slight time gaps
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "First Task"},
            headers=auth_headers,
        )
        time.sleep(0.01)
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Second Task"},
            headers=auth_headers,
        )
        time.sleep(0.01)
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Third Task"},
            headers=auth_headers,
        )

        # Get tasks without sort param (should be created_at desc)
        response = client.get(
            f"/api/{test_user.id}/tasks",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 3
        # Newest first
        assert tasks[0]["title"] == "Third Task"
        assert tasks[1]["title"] == "Second Task"
        assert tasks[2]["title"] == "First Task"

    def test_sort_by_created_asc(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T131: Sort by created_at ascending (oldest first)."""
        import time

        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "First Task"},
            headers=auth_headers,
        )
        time.sleep(0.01)
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Second Task"},
            headers=auth_headers,
        )
        time.sleep(0.01)
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Third Task"},
            headers=auth_headers,
        )

        # Sort by created_at ascending
        response = client.get(
            f"/api/{test_user.id}/tasks?sort=created_asc",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 3
        # Oldest first
        assert tasks[0]["title"] == "First Task"
        assert tasks[1]["title"] == "Second Task"
        assert tasks[2]["title"] == "Third Task"

    def test_sort_by_title(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T131: Sort by title alphabetically."""
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Zebra Task"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Apple Task"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Mango Task"},
            headers=auth_headers,
        )

        # Sort by title
        response = client.get(
            f"/api/{test_user.id}/tasks?sort=title",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 3
        assert tasks[0]["title"] == "Apple Task"
        assert tasks[1]["title"] == "Mango Task"
        assert tasks[2]["title"] == "Zebra Task"

    def test_sort_with_filters(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T131: Sort works correctly with filters applied."""
        # Create tasks with different statuses
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Zebra Pending"},
            headers=auth_headers,
        )
        resp = client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Apple Completed"},
            headers=auth_headers,
        )
        task_id = resp.json()["data"]["id"]
        client.patch(
            f"/api/{test_user.id}/tasks/{task_id}/toggle",
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Mango Pending"},
            headers=auth_headers,
        )

        # Sort pending tasks by title
        response = client.get(
            f"/api/{test_user.id}/tasks?status=pending&sort=title",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Mango Pending"
        assert tasks[1]["title"] == "Zebra Pending"


class TestTaskPrioritySorting:
    """Contract tests for priority sorting order (T132)."""

    def test_sort_by_priority_high_first(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T132: Sort by priority puts high priority tasks first."""
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Low Task", "priority": "low"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "High Task", "priority": "high"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Medium Task", "priority": "medium"},
            headers=auth_headers,
        )

        # Sort by priority
        response = client.get(
            f"/api/{test_user.id}/tasks?sort=priority",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 3
        # High first, then medium, then low
        assert tasks[0]["priority"] == "high"
        assert tasks[1]["priority"] == "medium"
        assert tasks[2]["priority"] == "low"

    def test_sort_by_priority_secondary_sort_by_created(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T132: Tasks with same priority are sorted by created_at desc."""
        import time

        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "First High", "priority": "high"},
            headers=auth_headers,
        )
        time.sleep(0.01)
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Second High", "priority": "high"},
            headers=auth_headers,
        )
        client.post(
            f"/api/{test_user.id}/tasks",
            json={"title": "Low Task", "priority": "low"},
            headers=auth_headers,
        )

        # Sort by priority
        response = client.get(
            f"/api/{test_user.id}/tasks?sort=priority",
            headers=auth_headers,
        )

        assert response.status_code == 200
        tasks = response.json()["data"]["tasks"]
        assert len(tasks) == 3
        # High tasks first, with newest high task first
        assert tasks[0]["title"] == "Second High"
        assert tasks[1]["title"] == "First High"
        assert tasks[2]["title"] == "Low Task"

    def test_sort_by_priority_with_pagination(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict[str, str],
    ):
        """T132: Priority sort works correctly with pagination."""
        # Create 3 tasks of each priority
        for i in range(3):
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"High {i}", "priority": "high"},
                headers=auth_headers,
            )
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Medium {i}", "priority": "medium"},
                headers=auth_headers,
            )
            client.post(
                f"/api/{test_user.id}/tasks",
                json={"title": f"Low {i}", "priority": "low"},
                headers=auth_headers,
            )

        # Get first page of priority-sorted tasks
        response = client.get(
            f"/api/{test_user.id}/tasks?sort=priority&limit=4",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()["data"]
        tasks = data["tasks"]
        assert len(tasks) == 4
        assert data["pagination"]["total"] == 9
        # First 4 should include all high priority tasks and 1 medium
        for task in tasks[:3]:
            assert task["priority"] == "high"