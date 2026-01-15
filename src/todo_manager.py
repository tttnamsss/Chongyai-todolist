"""TodoManager for handling todo list operations."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import List, Optional

from models import TodoItem, Priority, Status

TODOS_FILE = "todos.json"


def load_todos() -> List[TodoItem]:
    if not os.path.exists(TODOS_FILE):
        return []
    with open(TODOS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return [TodoItem.from_dict(item) for item in data]
        except Exception:
            return []


def save_todos(todos: List[TodoItem]) -> None:
    data = [todo.to_dict() for todo in todos]
    with open(TODOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class TodoManager:
    def __init__(self):
        self.todos = load_todos()

    def save(self) -> None:
        save_todos(self.todos)

    def create_todo(self, title: str, details: str, priority: Priority, owner: str) -> TodoItem:
        todo = TodoItem(
            title=title,
            details=details,
            priority=priority,
            owner=owner,
        )
        self.todos.append(todo)
        self.save()
        return todo

    def get_todos_by_owner(self, owner: str) -> List[TodoItem]:
        return [todo for todo in self.todos if todo.owner == owner]

    def get_todo_by_id(self, todo_id: str, owner: str) -> Optional[TodoItem]:
        for todo in self.todos:
            if todo.id == todo_id and todo.owner == owner:
                return todo
        return None

    def update_todo(self, todo_id: str, owner: str, **updates) -> bool:
        todo = self.get_todo_by_id(todo_id, owner)
        if not todo:
            return False
        for key, value in updates.items():
            if hasattr(todo, key):
                setattr(todo, key, value)
        todo.updated_at = datetime.now(timezone.utc).isoformat() + "Z"
        self.save()
        return True

    def mark_completed(self, todo_id: str, owner: str) -> bool:
        return self.update_todo(todo_id, owner, status=Status.COMPLETED)

    def delete_todo(self, todo_id: str, owner: str) -> bool:
        todo = self.get_todo_by_id(todo_id, owner)
        if not todo:
            return False
        self.todos.remove(todo)
        self.save()
        return True