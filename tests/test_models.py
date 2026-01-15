"""Unit tests for data models in src/models.py."""

from models import TodoItem, Priority, Status


class TestPriority:
    def test_enum_values(self):
        assert Priority.HIGH.value == "HIGH"
        assert Priority.MID.value == "MID"
        assert Priority.LOW.value == "LOW"


class TestStatus:
    def test_enum_values(self):
        assert Status.PENDING.value == "PENDING"
        assert Status.COMPLETED.value == "COMPLETED"


class TestTodoItem:
    def test_creation_with_defaults(self):
        item = TodoItem()
        assert item.title == ""
        assert item.details == ""
        assert item.priority == Priority.MID
        assert item.status == Status.PENDING
        assert item.owner is None
        assert isinstance(item.id, str)
        assert len(item.id) == 36  # UUID length
        assert item.created_at.endswith("Z")
        assert item.updated_at.endswith("Z")

    def test_creation_with_values(self):
        item = TodoItem(
            title="Test Todo",
            details="Test details",
            priority=Priority.HIGH,
            status=Status.COMPLETED,
            owner="testuser",
        )
        assert item.title == "Test Todo"
        assert item.details == "Test details"
        assert item.priority == Priority.HIGH
        assert item.status == Status.COMPLETED
        assert item.owner == "testuser"

    def test_to_dict(self):
        item = TodoItem(
            id="test-id",
            title="Test Todo",
            details="Test details",
            priority=Priority.HIGH,
            status=Status.COMPLETED,
            owner="testuser",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )
        d = item.to_dict()
        expected = {
            "id": "test-id",
            "title": "Test Todo",
            "details": "Test details",
            "priority": "HIGH",
            "status": "COMPLETED",
            "owner": "testuser",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
        }
        assert d == expected

    def test_from_dict(self):
        d = {
            "id": "test-id",
            "title": "Test Todo",
            "details": "Test details",
            "priority": "HIGH",
            "status": "COMPLETED",
            "owner": "testuser",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
        }
        item = TodoItem.from_dict(d)
        assert item.id == "test-id"
        assert item.title == "Test Todo"
        assert item.details == "Test details"
        assert item.priority == Priority.HIGH
        assert item.status == Status.COMPLETED
        assert item.owner == "testuser"
        assert item.created_at == "2023-01-01T00:00:00Z"
        assert item.updated_at == "2023-01-01T00:00:00Z"

    def test_from_dict_with_defaults(self):
        d = {"title": "Test Todo"}
        item = TodoItem.from_dict(d)
        assert item.title == "Test Todo"
        assert item.details == ""
        assert item.priority == Priority.MID
        assert item.status == Status.PENDING
        assert item.owner is None
        assert isinstance(item.id, str)
        assert item.created_at.endswith("Z")
        assert item.updated_at.endswith("Z")

    def test_uuid_uniqueness(self):
        item1 = TodoItem()
        item2 = TodoItem()
        assert item1.id != item2.id

    def test_datetime_fields(self):
        item = TodoItem()
        # Should be ISO format with Z
        assert "T" in item.created_at
        assert item.created_at.endswith("Z")
        assert "T" in item.updated_at
        assert item.updated_at.endswith("Z")
