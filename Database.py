import sqlite3

class Database:
    def __init__(self, db_path="vcs.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.initialize_tables()

    def initialize_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_repositories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                repo_path TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        self.conn.commit()

    def delete_repository(self, repo_path):
        self.cursor.execute(
            "DELETE FROM user_repositories WHERE repo_path = ?",
            (repo_path,)
        )
        self.conn.commit()

    def add_user(self, username, password, is_admin=False):
        self.cursor.execute(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            (username, password, is_admin),
        )
        self.conn.commit()

    def authenticate_user(self, username, password):
        self.cursor.execute(
            "SELECT id, username, password, is_admin FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        return self.cursor.fetchone()

    def add_repository(self, user_id, repo_path):
        self.cursor.execute(
            "INSERT INTO user_repositories (user_id, repo_path) VALUES (?, ?)",
            (user_id, repo_path),
        )
        self.conn.commit()

    def is_admin(self, username):
        self.cursor.execute(
            "SELECT is_admin FROM users WHERE username = ?",
            (username,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else False


    def get_user_repositories(self, user_id):
        self.cursor.execute(
            "SELECT repo_path FROM user_repositories WHERE user_id = ?",
            (user_id,)
        )
        return [row[0] for row in self.cursor.fetchall()]

    def get_name_repositories(self, user_id):
        self.cursor.execute(
            "SELECT name FROM user_repositories WHERE user_id = ?",
            (user_id,)
        )
        return [row[0] for row in self.cursor.fetchall()]

    def get_user_id_by_username(self, username):
        self.cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_all_repositories(self):
        self.cursor.execute(
            """
            SELECT user_repositories.repo_path, users.username
            FROM users
            JOIN user_repositories ON users.id = user_repositories.user_id
            """
        )
        return self.cursor.fetchall()