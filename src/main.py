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


def main() -> None:
    user = pre_login_menu()
    if not user:
        return
    # Placeholder for post-login app loop. For now we exit after login.
    print(f"Logged in as: {user}. (Post-login features not yet implemented.)")


if __name__ == "__main__":
    main()
