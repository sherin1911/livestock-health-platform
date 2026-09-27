from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

import os
import sqlite3
from datetime import datetime

from backend.utils.authorization import get_current_identity


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth",
)


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "instance", "database.db")


def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def table_exists(connection, table_name):
    row = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    ).fetchone()

    return row is not None


def column_exists(connection, table_name, column_name):
    columns = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    for column in columns:
        if column["name"] == column_name:
            return True

    return False


def ensure_users_table():
    connection = get_db_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'FARMER',
                language TEXT DEFAULT 'en',
                status TEXT DEFAULT 'ACTIVE',
                created_at TEXT
            )
            """
        )

        # ----------------------------------------------------
        # Add missing columns to older databases
        # ----------------------------------------------------

        if not column_exists(connection, "users", "role"):
            connection.execute(
                """
                ALTER TABLE users
                ADD COLUMN role TEXT DEFAULT 'FARMER'
                """
            )

        if not column_exists(connection, "users", "language"):
            connection.execute(
                """
                ALTER TABLE users
                ADD COLUMN language TEXT DEFAULT 'en'
                """
            )

        if not column_exists(connection, "users", "status"):
            connection.execute(
                """
                ALTER TABLE users
                ADD COLUMN status TEXT DEFAULT 'ACTIVE'
                """
            )

        if not column_exists(connection, "users", "created_at"):
            connection.execute(
                """
                ALTER TABLE users
                ADD COLUMN created_at TEXT
                """
            )

        # ----------------------------------------------------
        # Repair empty values in existing users
        # ----------------------------------------------------

        connection.execute(
            """
            UPDATE users
            SET role = 'FARMER'
            WHERE role IS NULL OR TRIM(role) = ''
            """
        )

        connection.execute(
            """
            UPDATE users
            SET language = 'en'
            WHERE language IS NULL OR TRIM(language) = ''
            """
        )

        connection.execute(
            """
            UPDATE users
            SET status = 'ACTIVE'
            WHERE status IS NULL OR TRIM(status) = ''
            """
        )

        connection.execute(
            """
            UPDATE users
            SET created_at = ?
            WHERE created_at IS NULL OR TRIM(created_at) = ''
            """,
            (datetime.utcnow().isoformat(),),
        )

        connection.commit()

    finally:
        connection.close()


# Create/upgrade the users table when this module loads.
ensure_users_table()


# ============================================================
# HELPERS
# ============================================================

ALLOWED_ROLES = {
    "FARMER",
    "FIELD_WORKER",
    "VETERINARIAN",
    "LAB_STAFF",
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN",
}

ALLOWED_LANGUAGES = {
    "en",
    "ta",
    "mr",
    "hi",
}


def normalize_role(role):
    if not role:
        return "FARMER"

    role = str(role).strip().upper()

    if role not in ALLOWED_ROLES:
        return "FARMER"

    return role


def normalize_language(language):
    if not language:
        return "en"

    language = str(language).strip().lower()

    if language not in ALLOWED_LANGUAGES:
        return "en"

    return language


def serialize_user(user):
    if user is None:
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "username": user["username"],
        "role": normalize_role(user["role"]),
        "language": normalize_language(user["language"]),
        "status": user["status"] or "ACTIVE",
        "createdAt": user["created_at"],
    }


def create_user_token(user):
    identity = {
        "user_id": user["id"],
        "username": user["username"],
        "role": normalize_role(user["role"]),
    }

    return create_access_token(identity=identity)


def get_identity_from_token():
    identity = get_jwt_identity()

    if isinstance(identity, dict):
        return identity

    # Backward compatibility if an older token contains only username.
    if isinstance(identity, str):
        return {
            "username": identity,
        }

    return {}


def get_user_by_id(user_id):
    connection = get_db_connection()

    try:
        return connection.execute(
            """
            SELECT
                id,
                name,
                email,
                username,
                password,
                role,
                language,
                status,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    finally:
        connection.close()


def get_user_by_username(username):
    connection = get_db_connection()

    try:
        return connection.execute(
            """
            SELECT
                id,
                name,
                email,
                username,
                password,
                role,
                language,
                status,
                created_at
            FROM users
            WHERE LOWER(username) = LOWER(?)
            """,
            (username,),
        ).fetchone()

    finally:
        connection.close()


def get_user_by_email(email):
    connection = get_db_connection()

    try:
        return connection.execute(
            """
            SELECT
                id,
                name,
                email,
                username,
                password,
                role,
                language,
                status,
                created_at
            FROM users
            WHERE LOWER(email) = LOWER(?)
            """,
            (email,),
        ).fetchone()

    finally:
        connection.close()


def extract_json():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {}

    return data


# ============================================================
# REGISTER
# ============================================================

@auth_bp.route("/register", methods=["POST"])
def register():
    data = extract_json()

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))
    language = normalize_language(data.get("language", "en"))

    if not name:
        return jsonify(
            {
                "success": False,
                "message": "Name is required.",
            }
        ), 400

    if not email:
        return jsonify(
            {
                "success": False,
                "message": "Email is required.",
            }
        ), 400

    if not username:
        return jsonify(
            {
                "success": False,
                "message": "Username is required.",
            }
        ), 400

    if not password:
        return jsonify(
            {
                "success": False,
                "message": "Password is required.",
            }
        ), 400

    if len(password) < 6:
        return jsonify(
            {
                "success": False,
                "message": "Password must contain at least 6 characters.",
            }
        ), 400

    connection = get_db_connection()

    try:
        existing_username = connection.execute(
            """
            SELECT id
            FROM users
            WHERE LOWER(username) = LOWER(?)
            """,
            (username,),
        ).fetchone()

        if existing_username:
            return jsonify(
                {
                    "success": False,
                    "message": "Username already exists.",
                }
            ), 409

        existing_email = connection.execute(
            """
            SELECT id
            FROM users
            WHERE LOWER(email) = LOWER(?)
            """,
            (email,),
        ).fetchone()

        if existing_email:
            return jsonify(
                {
                    "success": False,
                    "message": "Email already registered.",
                }
            ), 409

        password_hash = generate_password_hash(password)
        created_at = datetime.utcnow().isoformat()

        # Public registration creates FARMER accounts.
        role = "FARMER"

        cursor = connection.execute(
            """
            INSERT INTO users (
                name,
                email,
                username,
                password,
                role,
                language,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                username,
                password_hash,
                role,
                language,
                "ACTIVE",
                created_at,
            ),
        )

        connection.commit()

        user_id = cursor.lastrowid

        user = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                username,
                password,
                role,
                language,
                status,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        return jsonify(
            {
                "success": True,
                "message": "Registration successful.",
                "user": serialize_user(user),
            }
        ), 201

    except sqlite3.IntegrityError:
        connection.rollback()

        return jsonify(
            {
                "success": False,
                "message": "Username or email already exists.",
            }
        ), 409

    except sqlite3.Error as error:
        connection.rollback()

        return jsonify(
            {
                "success": False,
                "message": "Unable to create account.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# LOGIN
# ============================================================

@auth_bp.route("/login", methods=["POST"])
def login():
    data = extract_json()

    login_value = str(
        data.get("username")
        or data.get("email")
        or data.get("login")
        or ""
    ).strip()

    password = str(data.get("password", ""))

    if not login_value:
        return jsonify(
            {
                "success": False,
                "message": "Username or email is required.",
            }
        ), 400

    if not password:
        return jsonify(
            {
                "success": False,
                "message": "Password is required.",
            }
        ), 400

    connection = get_db_connection()

    try:
        user = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                username,
                password,
                role,
                language,
                status,
                created_at
            FROM users
            WHERE LOWER(username) = LOWER(?)
               OR LOWER(email) = LOWER(?)
            LIMIT 1
            """,
            (
                login_value,
                login_value,
            ),
        ).fetchone()

        if user is None:
            return jsonify(
                {
                    "success": False,
                    "message": "Invalid username/email or password.",
                }
            ), 401

        stored_password = user["password"] or ""

        try:
            password_valid = check_password_hash(
                stored_password,
                password,
            )
        except (ValueError, TypeError):
            password_valid = False

        if not password_valid:
            return jsonify(
                {
                    "success": False,
                    "message": "Invalid username/email or password.",
                }
            ), 401

        user_status = str(
            user["status"] or "ACTIVE"
        ).upper()

        if user_status != "ACTIVE":
            return jsonify(
                {
                    "success": False,
                    "message": "This account is currently inactive.",
                }
            ), 403

        token = create_user_token(user)

        return jsonify(
            {
                "success": True,
                "message": "Login successful.",
                "access_token": token,
                "token": token,
                "user": serialize_user(user),
            }
        ), 200

    except sqlite3.Error as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to process login.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# CURRENT USER
# ============================================================

@auth_bp.route("/me", methods=["GET"])
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def current_user():
    identity = get_identity_from_token()

    user_id = identity.get("user_id")
    username = identity.get("username")

    user = None

    if user_id is not None:
        user = get_user_by_id(user_id)

    if user is None and username:
        user = get_user_by_username(username)

    if user is None:
        return jsonify(
            {
                "success": False,
                "message": "User account not found.",
            }
        ), 404

    if str(user["status"] or "ACTIVE").upper() != "ACTIVE":
        return jsonify(
            {
                "success": False,
                "message": "This account is inactive.",
            }
        ), 403

    return jsonify(
        {
            "success": True,
            "user": serialize_user(user),
        }
    ), 200


# ============================================================
# UPDATE PROFILE
# ============================================================

@auth_bp.route("/profile", methods=["PUT", "PATCH"])
@jwt_required()
def update_profile():
    identity = get_identity_from_token()

    user_id = identity.get("user_id")
    username_from_token = identity.get("username")

    data = extract_json()

    name = data.get("name")
    email = data.get("email")
    language = data.get("language")

    user = None

    if user_id is not None:
        user = get_user_by_id(user_id)

    if user is None and username_from_token:
        user = get_user_by_username(username_from_token)

    if user is None:
        return jsonify(
            {
                "success": False,
                "message": "User account not found.",
            }
        ), 404

    new_name = (
        str(name).strip()
        if name is not None
        else user["name"]
    )

    new_email = (
        str(email).strip().lower()
        if email is not None
        else user["email"]
    )

    new_language = (
        normalize_language(language)
        if language is not None
        else normalize_language(user["language"])
    )

    if not new_name:
        return jsonify(
            {
                "success": False,
                "message": "Name cannot be empty.",
            }
        ), 400

    if not new_email:
        return jsonify(
            {
                "success": False,
                "message": "Email cannot be empty.",
            }
        ), 400

    connection = get_db_connection()

    try:
        duplicate = connection.execute(
            """
            SELECT id
            FROM users
            WHERE LOWER(email) = LOWER(?)
            AND id != ?
            """,
            (
                new_email,
                user["id"],
            ),
        ).fetchone()

        if duplicate:
            return jsonify(
                {
                    "success": False,
                    "message": "Email is already used by another account.",
                }
            ), 409

        connection.execute(
            """
            UPDATE users
            SET
                name = ?,
                email = ?,
                language = ?
            WHERE id = ?
            """,
            (
                new_name,
                new_email,
                new_language,
                user["id"],
            ),
        )

        connection.commit()

        updated_user = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                username,
                password,
                role,
                language,
                status,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user["id"],),
        ).fetchone()

        return jsonify(
            {
                "success": True,
                "message": "Profile updated successfully.",
                "user": serialize_user(updated_user),
            }
        ), 200

    except sqlite3.Error as error:
        connection.rollback()

        return jsonify(
            {
                "success": False,
                "message": "Unable to update profile.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# CHANGE LANGUAGE
# ============================================================

@auth_bp.route("/language", methods=["PUT", "PATCH"])
@jwt_required()
def change_language():
    identity = get_identity_from_token()

    user_id = identity.get("user_id")
    username_from_token = identity.get("username")

    data = extract_json()

    language = normalize_language(data.get("language"))

    user = None

    if user_id is not None:
        user = get_user_by_id(user_id)

    if user is None and username_from_token:
        user = get_user_by_username(username_from_token)

    if user is None:
        return jsonify(
            {
                "success": False,
                "message": "User account not found.",
            }
        ), 404

    connection = get_db_connection()

    try:
        connection.execute(
            """
            UPDATE users
            SET language = ?
            WHERE id = ?
            """,
            (
                language,
                user["id"],
            ),
        )

        connection.commit()

        updated_user = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                username,
                password,
                role,
                language,
                status,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user["id"],),
        ).fetchone()

        return jsonify(
            {
                "success": True,
                "message": "Language updated successfully.",
                "language": language,
                "user": serialize_user(updated_user),
            }
        ), 200

    except sqlite3.Error as error:
        connection.rollback()

        return jsonify(
            {
                "success": False,
                "message": "Unable to update language.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# CHANGE PASSWORD
# ============================================================

@auth_bp.route("/change-password", methods=["PUT", "POST"])
@jwt_required()
def change_password():
    identity = get_identity_from_token()

    user_id = identity.get("user_id")
    username_from_token = identity.get("username")

    data = extract_json()

    current_password = str(
        data.get("currentPassword")
        or data.get("current_password")
        or ""
    )

    new_password = str(
        data.get("newPassword")
        or data.get("new_password")
        or ""
    )

    confirm_password = str(
        data.get("confirmPassword")
        or data.get("confirm_password")
        or ""
    )

    user = None

    if user_id is not None:
        user = get_user_by_id(user_id)

    if user is None and username_from_token:
        user = get_user_by_username(username_from_token)

    if user is None:
        return jsonify(
            {
                "success": False,
                "message": "User account not found.",
            }
        ), 404

    if not current_password:
        return jsonify(
            {
                "success": False,
                "message": "Current password is required.",
            }
        ), 400

    if not new_password:
        return jsonify(
            {
                "success": False,
                "message": "New password is required.",
            }
        ), 400

    if len(new_password) < 6:
        return jsonify(
            {
                "success": False,
                "message": "New password must contain at least 6 characters.",
            }
        ), 400

    if confirm_password and new_password != confirm_password:
        return jsonify(
            {
                "success": False,
                "message": "New password and confirmation do not match.",
            }
        ), 400

    try:
        current_password_valid = check_password_hash(
            user["password"],
            current_password,
        )
    except (ValueError, TypeError):
        current_password_valid = False

    if not current_password_valid:
        return jsonify(
            {
                "success": False,
                "message": "Current password is incorrect.",
            }
        ), 401

    if current_password == new_password:
        return jsonify(
            {
                "success": False,
                "message": "New password must be different from the current password.",
            }
        ), 400

    new_password_hash = generate_password_hash(new_password)

    connection = get_db_connection()

    try:
        connection.execute(
            """
            UPDATE users
            SET password = ?
            WHERE id = ?
            """,
            (
                new_password_hash,
                user["id"],
            ),
        )

        connection.commit()

        return jsonify(
            {
                "success": True,
                "message": "Password changed successfully.",
            }
        ), 200

    except sqlite3.Error as error:
        connection.rollback()

        return jsonify(
            {
                "success": False,
                "message": "Unable to change password.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# LOGOUT
# ============================================================

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify(
        {
            "success": True,
            "message": (
                "Logout successful. "
                "Please remove the stored access token from the browser."
            ),
        }
    ), 200


# ============================================================
# AUTHENTICATION STATUS
# ============================================================

@auth_bp.route("/status", methods=["GET"])
def auth_status():
    return jsonify(
        {
            "success": True,
            "status": "operational",
            "authentication": True,
            "jwt": True,
        }
    ), 200


# ============================================================
# CURRENT USER STATUS
# ============================================================

@auth_bp.route("/session", methods=["GET"])
@jwt_required()
def session_status():
    identity = get_current_identity()

    if not identity:
        return jsonify(
            {
                "success": False,
                "authenticated": False,
                "message": "No valid user session found.",
            }
        ), 401

    user_id = identity.get("user_id")
    username = identity.get("username")

    user = None

    if user_id is not None:
        user = get_user_by_id(user_id)

    if user is None and username:
        user = get_user_by_username(username)

    if user is None:
        return jsonify(
            {
                "success": False,
                "authenticated": False,
                "message": "User account not found.",
            }
        ), 404

    if str(user["status"] or "ACTIVE").upper() != "ACTIVE":
        return jsonify(
            {
                "success": False,
                "authenticated": False,
                "message": "User account is inactive.",
            }
        ), 403

    return jsonify(
        {
            "success": True,
            "authenticated": True,
            "user": serialize_user(user),
        }
    ), 200