from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

import sqlite3
import os
from datetime import datetime

from backend.utils.authorization import role_required


# ============================================================
# BLUEPRINT
# ============================================================

investigations_bp = Blueprint(
    "investigations",
    __name__,
    url_prefix="/api/investigations"
)


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "instance",
    "database.db"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    os.makedirs(
        os.path.dirname(DB_PATH),
        exist_ok=True
    )

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# CREATE INVESTIGATIONS TABLE
# ============================================================

def ensure_investigations_table():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS investigations (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                report_id TEXT UNIQUE NOT NULL,

                veterinarian_username TEXT,

                status TEXT DEFAULT 'UNDER INVESTIGATION',

                temperature TEXT,

                respiration TEXT,

                hydration TEXT,

                appetite TEXT,

                behaviour TEXT,

                visible_signs TEXT,

                sample_type TEXT,

                collection_date TEXT,

                collection_notes TEXT,

                preliminary_assessment TEXT,

                surveillance_flag INTEGER DEFAULT 0,

                created_at TEXT NOT NULL,

                updated_at TEXT NOT NULL

            )
            """
        )

        connection.commit()

    finally:

        connection.close()


# ============================================================
# HEALTH REPORT TABLE CHECK
# ============================================================

def ensure_health_reports_table():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS health_reports (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                report_id TEXT UNIQUE NOT NULL,

                username TEXT,

                animal_name TEXT NOT NULL,

                species TEXT NOT NULL,

                severity TEXT NOT NULL,

                symptoms TEXT,

                description TEXT,

                location TEXT,

                latitude REAL,

                longitude REAL,

                risk_score INTEGER DEFAULT 0,

                risk_level TEXT,

                photo_name TEXT,

                audio_name TEXT,

                status TEXT DEFAULT 'NEW',

                created_at TEXT NOT NULL

            )
            """
        )

        connection.commit()

    finally:

        connection.close()


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user():

    identity = get_jwt_identity()

    if isinstance(identity, dict):

        return {
            "user_id": identity.get("user_id"),
            "username": identity.get("username"),
            "role": str(
                identity.get("role") or ""
            ).upper()
        }

    return {
        "user_id": None,
        "username": identity,
        "role": ""
    }


# ============================================================
# VALIDATE STATUS
# ============================================================

ALLOWED_STATUSES = {
    "NEW",
    "UNDER INVESTIGATION",
    "SENT TO LAB",
    "VALIDATED",
    "REJECTED"
}


def normalize_status(status):

    value = str(
        status or "UNDER INVESTIGATION"
    ).strip().upper()

    if value not in ALLOWED_STATUSES:
        return None

    return value


# ============================================================
# POST /api/investigations
# CREATE OR UPDATE INVESTIGATION
# ============================================================

@investigations_bp.route(
    "",
    methods=["POST"]
)
@role_required(
    "VETERINARIAN"
)
def save_investigation():

    ensure_investigations_table()
    ensure_health_reports_table()

    data = request.get_json(
        silent=True
    ) or {}

    user = get_current_user()

    veterinarian_username = (
        user.get("username")
    )

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    report_id = str(
        data.get("reportId")
        or data.get("report_id")
        or ""
    ).strip()

    status = normalize_status(
        data.get("status")
    )

    temperature = str(
        data.get("temperature")
        or ""
    ).strip()

    respiration = str(
        data.get("respiration")
        or ""
    ).strip()

    hydration = str(
        data.get("hydration")
        or ""
    ).strip()

    appetite = str(
        data.get("appetite")
        or ""
    ).strip()

    behaviour = str(
        data.get("behaviour")
        or ""
    ).strip()

    visible_signs = str(
        data.get("visibleSigns")
        or data.get("visible_signs")
        or ""
    ).strip()

    sample_type = str(
        data.get("sampleType")
        or data.get("sample_type")
        or ""
    ).strip()

    collection_date = str(
        data.get("collectionDate")
        or data.get("collection_date")
        or ""
    ).strip()

    collection_notes = str(
        data.get("collectionNotes")
        or data.get("collection_notes")
        or ""
    ).strip()

    preliminary_assessment = str(
        data.get("preliminaryAssessment")
        or data.get("preliminary_assessment")
        or ""
    ).strip()

    surveillance_flag = data.get(
        "surveillanceFlag",
        0
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not report_id:

        return jsonify({
            "success": False,
            "message":
                "Report ID is required."
        }), 400

    if not status:

        return jsonify({
            "success": False,
            "message":
                "Invalid investigation status."
        }), 400

    try:

        surveillance_flag = (
            1
            if bool(
                surveillance_flag
            )
            else 0
        )

    except Exception:

        surveillance_flag = 0

    # --------------------------------------------------------
    # CHECK REPORT
    # --------------------------------------------------------

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT report_id
            FROM health_reports
            WHERE report_id = ?
            LIMIT 1
            """,
            (
                report_id,
            )
        )

        report = cursor.fetchone()

    finally:

        connection.close()

    if not report:

        return jsonify({
            "success": False,
            "message":
                "Health report not found."
        }), 404

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # --------------------------------------------------------
    # UPSERT INVESTIGATION
    # --------------------------------------------------------

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM investigations
            WHERE report_id = ?
            LIMIT 1
            """,
            (
                report_id,
            )
        )

        existing = cursor.fetchone()

        if existing:

            cursor.execute(
                """
                UPDATE investigations
                SET
                    veterinarian_username = ?,
                    status = ?,
                    temperature = ?,
                    respiration = ?,
                    hydration = ?,
                    appetite = ?,
                    behaviour = ?,
                    visible_signs = ?,
                    sample_type = ?,
                    collection_date = ?,
                    collection_notes = ?,
                    preliminary_assessment = ?,
                    surveillance_flag = ?,
                    updated_at = ?
                WHERE report_id = ?
                """,
                (
                    veterinarian_username,
                    status,
                    temperature,
                    respiration,
                    hydration,
                    appetite,
                    behaviour,
                    visible_signs,
                    sample_type,
                    collection_date,
                    collection_notes,
                    preliminary_assessment,
                    surveillance_flag,
                    now,
                    report_id
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO investigations (
                    report_id,
                    veterinarian_username,
                    status,
                    temperature,
                    respiration,
                    hydration,
                    appetite,
                    behaviour,
                    visible_signs,
                    sample_type,
                    collection_date,
                    collection_notes,
                    preliminary_assessment,
                    surveillance_flag,
                    created_at,
                    updated_at
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    report_id,
                    veterinarian_username,
                    status,
                    temperature,
                    respiration,
                    hydration,
                    appetite,
                    behaviour,
                    visible_signs,
                    sample_type,
                    collection_date,
                    collection_notes,
                    preliminary_assessment,
                    surveillance_flag,
                    now,
                    now
                )
            )

        # ----------------------------------------------------
        # UPDATE HEALTH REPORT STATUS
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE health_reports
            SET status = ?
            WHERE report_id = ?
            """,
            (
                status,
                report_id
            )
        )

        connection.commit()

        # ----------------------------------------------------
        # RETURN SAVED RECORD
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                report_id,
                veterinarian_username,
                status,
                temperature,
                respiration,
                hydration,
                appetite,
                behaviour,
                visible_signs,
                sample_type,
                collection_date,
                collection_notes,
                preliminary_assessment,
                surveillance_flag,
                created_at,
                updated_at
            FROM investigations
            WHERE report_id = ?
            LIMIT 1
            """,
            (
                report_id,
            )
        )

        row = cursor.fetchone()

        investigation = dict(row)

    finally:

        connection.close()

    return jsonify({

        "success": True,

        "message":
            "Investigation saved successfully.",

        "investigation":
            investigation

    }), 200


# ============================================================
# GET SINGLE INVESTIGATION
# ============================================================

@investigations_bp.route(
    "/<report_id>",
    methods=["GET"]
)
@role_required(
    "VETERINARIAN",
    "LAB_STAFF",
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN"
)
def get_investigation(
    report_id
):

    ensure_investigations_table()

    report_id = str(
        report_id
    ).strip()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                report_id,
                veterinarian_username,
                status,
                temperature,
                respiration,
                hydration,
                appetite,
                behaviour,
                visible_signs,
                sample_type,
                collection_date,
                collection_notes,
                preliminary_assessment,
                surveillance_flag,
                created_at,
                updated_at
            FROM investigations
            WHERE report_id = ?
            LIMIT 1
            """,
            (
                report_id,
            )
        )

        row = cursor.fetchone()

        if not row:

            return jsonify({
                "success": False,
                "message":
                    "Investigation not found."
            }), 404

        return jsonify({

            "success": True,

            "investigation":
                dict(row)

        }), 200

    finally:

        connection.close()


# ============================================================
# GET ALL INVESTIGATIONS
# ============================================================

@investigations_bp.route(
    "",
    methods=["GET"]
)
@role_required(
    "VETERINARIAN",
    "LAB_STAFF",
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN"
)
def get_all_investigations():

    ensure_investigations_table()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                report_id,
                veterinarian_username,
                status,
                temperature,
                respiration,
                hydration,
                appetite,
                behaviour,
                visible_signs,
                sample_type,
                collection_date,
                collection_notes,
                preliminary_assessment,
                surveillance_flag,
                created_at,
                updated_at
            FROM investigations
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        investigations = [
            dict(row)
            for row in rows
        ]

        return jsonify({

            "success": True,

            "investigations":
                investigations,

            "count":
                len(investigations)

        }), 200

    finally:

        connection.close()


# ============================================================
# UPDATE STATUS ONLY
# ============================================================

@investigations_bp.route(
    "/<report_id>/status",
    methods=["PUT"]
)
@role_required(
    "VETERINARIAN",
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN"
)
def update_investigation_status(
    report_id
):

    ensure_investigations_table()
    ensure_health_reports_table()

    data = request.get_json(
        silent=True
    ) or {}

    status = normalize_status(
        data.get("status")
    )

    if not status:

        return jsonify({
            "success": False,
            "message":
                "Invalid investigation status."
        }), 400

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE investigations
            SET
                status = ?,
                updated_at = ?
            WHERE report_id = ?
            """,
            (
                status,
                now,
                report_id
            )
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return jsonify({
                "success": False,
                "message":
                    "Investigation not found."
            }), 404

        cursor.execute(
            """
            UPDATE health_reports
            SET status = ?
            WHERE report_id = ?
            """,
            (
                status,
                report_id
            )
        )

        connection.commit()

        cursor.execute(
            """
            SELECT
                id,
                report_id,
                veterinarian_username,
                status,
                temperature,
                respiration,
                hydration,
                appetite,
                behaviour,
                visible_signs,
                sample_type,
                collection_date,
                collection_notes,
                preliminary_assessment,
                surveillance_flag,
                created_at,
                updated_at
            FROM investigations
            WHERE report_id = ?
            LIMIT 1
            """,
            (
                report_id,
            )
        )

        row = cursor.fetchone()

        return jsonify({

            "success": True,

            "message":
                "Investigation status updated.",

            "investigation":
                dict(row)

        }), 200

    finally:

        connection.close()


# ============================================================
# MODULE STATUS
# ============================================================

@investigations_bp.route(
    "/status",
    methods=["GET"]
)
@jwt_required()
def investigation_status():

    ensure_investigations_table()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM investigations
            """
        )

        row = cursor.fetchone()

        count = int(
            row[0] or 0
        )

    finally:

        connection.close()

    return jsonify({

        "success": True,

        "module":
            "Veterinary Investigations",

        "status":
            "active",

        "investigationCount":
            count

    }), 200
