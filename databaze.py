
import sqlite3
import hashlib
import secrets
import hmac
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "utulek.db"


class Databaze:
    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self.vytvor_tabulky()

    def pripojeni(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def vytvor_tabulky(self):
        with self.pripojeni() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    password_hash TEXT NOT NULL,
                    password_salt TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS dogs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    breed TEXT,
                    age INTEGER,
                    description TEXT,
                    image_path TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

    @staticmethod
    def vytvor_hash(password, salt):
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            300_000
        ).hex()

    def vytvor_ucet(self, username, password):
        username = username.strip()

        if not username or not password:
            return False, "Please fill in all fields."

        if len(username) > 50:
            return False, "Username is too long."

        if len(password) < 4:
            return False, "Password must have at least 4 characters."

        if len(password) > 8:
            return False, "Password can have at most 8 characters."

        salt = secrets.token_bytes(16)
        password_hash = self.vytvor_hash(password, salt)

        try:
            with self.pripojeni() as conn:
                conn.execute("""
                    INSERT INTO users
                        (username, password_hash, password_salt)
                    VALUES (?, ?, ?)
                """, (username, password_hash, salt.hex()))

            return True, "Account created successfully!"

        except sqlite3.IntegrityError:
            return False, "This username already exists."

    def over_ucet(self, username, password):
        with self.pripojeni() as conn:
            user = conn.execute("""
                SELECT id, username, password_hash, password_salt
                FROM users
                WHERE username = ?
            """, (username.strip(),)).fetchone()

        if user is None:
            return None

        salt = bytes.fromhex(user["password_salt"])
        password_hash = self.vytvor_hash(password, salt)

        if hmac.compare_digest(password_hash, user["password_hash"]):
            return {
                "id": user["id"],
                "username": user["username"]
            }

        return None

    def seznam_psu(self):
        with self.pripojeni() as conn:
            dogs = conn.execute("""
                SELECT id, name, breed, age, description, image_path
                FROM dogs
                ORDER BY id DESC
            """).fetchall()

        return [dict(dog) for dog in dogs]

    def pridej_psa(
        self, name, breed="", age=None,
        description="", image_path=None
    ):
        name = name.strip()

        if not name:
            raise ValueError("Dog name is required.")

        if age is not None and (
            not isinstance(age, int) or age < 0
        ):
            raise ValueError("Age must be a non-negative integer.")

        with self.pripojeni() as conn:
            cursor = conn.execute("""
                INSERT INTO dogs
                    (name, breed, age, description, image_path)
                VALUES (?, ?, ?, ?, ?)
            """, (
                name, breed.strip(), age,
                description.strip(), image_path
            ))

            return cursor.lastrowid

        
    def smaz_uzivatele(self, user_id):
        with self.pripojeni() as conn:
            cursor = conn.execute(
                "DELETE FROM users WHERE id = ?",
                (user_id,)
            )
            return cursor.rowcount > 0

