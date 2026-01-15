"""Simple CLI entrypoint with pre-login menu (Login / Sign Up / Exit).

This implements a minimal `users.json` backing store for sign up and login
so the app can be exercised. Passwords are stored as plain text here for
simplicity — this can be replaced with hashed storage later.
"""

from __future__ import annotations

import json
import os
from getpass import getpass
from typing import Dict, List

from models import Priority, Status
from todo_manager import TodoManager

USERS_FILE = "users.json"


def load_users() -> List[Dict[str, str]]:
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []


def save_users(users: List[Dict[str, str]]) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def signup() -> None:
    users = load_users()
    username = input("Choose a username: ").strip()
    if any(u["username"] == username for u in users):
        print("Username already exists.")
        return
    password = getpass("Choose a password: ")
    users.append({"username": username, "password": password})
    save_users(users)
    print("Sign up successful. You can now log in.")


def login() -> str | None:
    users = load_users()
    username = input("Username: ").strip()
    password = getpass("Password: ")
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            print(f"Login successful. Welcome, {username}!")
            return username
    print("Invalid credentials.")
    return None


def pre_login_menu() -> str | None:
    while True:
        print("\nPre-Login Menu")
        print("1) Login")
        print("2) Sign Up")
        print("3) Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            user = login()
            if user:
                return user
        elif choice == "2":
            signup()
        elif choice == "3":
            print("Goodbye.")
            return None
        else:
            print("Invalid choice. Try again.")


def post_login_menu(user: str) -> None:
    manager = TodoManager()
    while True:
        print(f"\nLogged in as: {user}")
        print("Todo List Menu")
        print("1) View all to-do-list items")
        print("2) View to-do-list item details")
        print("3) Create a new to-do-list item")
        print("4) Edit a to-do-list item")
        print("5) Mark a to-do-list item as completed")
        print("6) Logout")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            view_all_todos(manager, user)
        elif choice == "2":
            view_todo_details(manager, user)
        elif choice == "3":
            create_todo(manager, user)
        elif choice == "4":
            edit_todo(manager, user)
        elif choice == "5":
            mark_completed(manager, user)
        elif choice == "6":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Try again.")


def view_all_todos(manager: TodoManager, user: str) -> None:
    todos = manager.get_todos_by_owner(user)
    if not todos:
        print("No todos found.")
        return
    print("\nYour Todos:")
    for todo in todos:
        status = "✓" if todo.status == Status.COMPLETED else "○"
        print(f"{status} {todo.title} (ID: {todo.id})")


def view_todo_details(manager: TodoManager, user: str) -> None:
    todo_id = input("Enter todo ID: ").strip()
    todo = manager.get_todo_by_id(todo_id, user)
    if not todo:
        print("Todo not found.")
        return
    print("\nTodo Details:")
    print(f"ID: {todo.id}")
    print(f"Title: {todo.title}")
    print(f"Details: {todo.details}")
    print(f"Priority: {todo.priority.value}")
    print(f"Status: {todo.status.value}")
    print(f"Owner: {todo.owner}")
    print(f"Created: {todo.created_at}")
    print(f"Updated: {todo.updated_at}")


def create_todo(manager: TodoManager, user: str) -> None:
    title = input("Title: ").strip()
    details = input("Details: ").strip()
    priority_str = input("Priority (HIGH/MID/LOW): ").strip().upper()
    try:
        priority = Priority(priority_str)
    except ValueError:
        print("Invalid priority. Using MID.")
        priority = Priority.MID
    todo = manager.create_todo(title, details, priority, user)
    print(f"Todo created with ID: {todo.id}")


def edit_todo(manager: TodoManager, user: str) -> None:
    todo_id = input("Enter todo ID to edit: ").strip()
    todo = manager.get_todo_by_id(todo_id, user)
    if not todo:
        print("Todo not found.")
        return
    print("Leave blank to keep current value.")
    title = input(f"Title ({todo.title}): ").strip()
    details = input(f"Details ({todo.details}): ").strip()
    priority_str = input(f"Priority ({todo.priority.value}): ").strip().upper()
    updates = {}
    if title:
        updates["title"] = title
    if details:
        updates["details"] = details
    if priority_str:
        try:
            updates["priority"] = Priority(priority_str)
        except ValueError:
            print("Invalid priority. Skipping.")
    if updates:
        success = manager.update_todo(todo_id, user, **updates)
        if success:
            print("Todo updated.")
        else:
            print("Failed to update todo.")
    else:
        print("No changes made.")


def mark_completed(manager: TodoManager, user: str) -> None:
    todo_id = input("Enter todo ID to mark as completed: ").strip()
    success = manager.mark_completed(todo_id, user)
    if success:
        print("Todo marked as completed.")
    else:
        print("Todo not found.")


def main() -> None:
    user = pre_login_menu()
    if not user:
        return
    post_login_menu(user)


if __name__ == "__main__":
    main()
