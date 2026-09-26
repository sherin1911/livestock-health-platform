from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

import sqlite3
import os
import uuid
from datetime import datetime

from services.notification_service import notify_for_report
from services.cluster_engine import build_location_clusters
from utils.authorization import role_required


# ============================================================
# BLUEPRINT
# ============================================================

health_reports_bp = Blueprint(
    "health_reports",
    __name__,
    url_prefix="/api/health-reports"
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

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# CREATE TABLE
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
# RISK CALCULATION
# ============================================================

def calculate_risk(severity, symptoms):
    severity_value = str(
        severity or ""
    ).strip().upper()

    base_scores = {
        "LOW": 15,
        "MEDIUM": 35,
        "HIGH": 60
    }

    score = base_scores.get(
        severity_value,
        15
    )

    symptom_count = 0

    if isinstance(symptoms, list):

        symptom_count = len(
            [
                item
                for item in symptoms
                if str(item).strip()
            ]
        )

    elif symptoms:

        raw = str(symptoms)

        for separator in [",", ";", "|"]:
            raw = raw.replace(
                separator,
                ","
            )

        symptom_count = len(
            [
                item
                for item in raw.split(",")
                if item.strip()
            ]
        )

    score += symptom_count * 8

    score = min(
        score,
        100
    )

    if score >= 60:
        risk_level = "HIGH"

    elif score >= 30:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return score, risk_level


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user_data():
    identity = get_jwt_identity()

    if isinstance(identity, dict):

        return {
            "user_id": identity.get("user_id"),
            "username": identity.get("username"),
            "role": str(
                identity.get("role") or "FARMER"
            ).upper()
        }

    return {
        "user_id": None,
        "username": identity,
        "role": "FARMER"
    }


# ============================================================
# NORMALIZE SYMPTOMS
# ============================================================

def normalize_symptoms(symptoms):

    if isinstance(symptoms, list):

        cleaned = [
            str(item).strip()
            for item in symptoms
            if str(item).strip()
        ]

        return ", ".join(cleaned)

    return str(
        symptoms or ""
    ).strip()


# ============================================================
# CREATE HEALTH REPORT
# ============================================================

@health_reports_bp.route(
    "",
    methods=["POST"]
)
@role_required(
    "FARMER",
    "FIELD_WORKER"
)
def create_health_report():

    ensure_health_reports_table()

    data = request.get_json(
        silent=True
    ) or {}

    user = get_current_user_data()

    username = user["username"]

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    animal_name = str(
        data.get("animalName")
        or data.get("animal_name")
        or ""
    ).strip()

    species = str(
        data.get("species")
        or ""
    ).strip()

    severity = str(
        data.get("severity")
        or "LOW"
    ).strip().upper()

    symptoms = data.get("symptoms")

    description = str(
        data.get("description")
        or ""
    ).strip()

    location = str(
        data.get("location")
        or ""
    ).strip()

    latitude = data.get("latitude")

    longitude = data.get("longitude")

    photo_name = (
        data.get("photoName")
        or data.get("photo_name")
    )

    audio_name = (
        data.get("audioName")
        or data.get("audio_name")
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not animal_name:

        return jsonify({
            "success": False,
            "message": "Animal name is required."
        }), 400

    if not species:

        return jsonify({
            "success": False,
            "message": "Species is required."
        }), 400

    if severity not in {
        "LOW",
        "MEDIUM",
        "HIGH"
    }:

        return jsonify({
            "success": False,
            "message": "Invalid severity."
        }), 400

    # --------------------------------------------------------
    # COORDINATES
    # --------------------------------------------------------

    try:

        if latitude in (
            None,
            "",
            "null"
        ):
            latitude = None
        else:
            latitude = float(latitude)

    except (
        TypeError,
        ValueError
    ):

        latitude = None

    try:

        if longitude in (
            None,
            "",
            "null"
        ):
            longitude = None
        else:
            longitude = float(longitude)

    except (
        TypeError,
        ValueError
    ):

        longitude = None

    # --------------------------------------------------------
    # SYMPTOMS
    # --------------------------------------------------------

    symptoms_text = normalize_symptoms(
        symptoms
    )

    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    risk_score, risk_level = calculate_risk(
        severity,
        symptoms_text
    )

    # --------------------------------------------------------
    # REPORT ID
    # --------------------------------------------------------

    report_id = (
        "RPT-"
        + datetime.now().strftime("%Y%m%d")
        + "-"
        + uuid.uuid4().hex[:6].upper()
    )

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # --------------------------------------------------------
    # SAVE REPORT
    # --------------------------------------------------------

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO health_reports (
                report_id,
                username,
                animal_name,
                species,
                severity,
                symptoms,
                description,
                location,
                latitude,
                longitude,
                risk_score,
                risk_level,
                photo_name,
                audio_name,
                status,
                created_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                report_id,
                username,
                animal_name,
                species,
                severity,
                symptoms_text,
                description,
                location,
                latitude,
                longitude,
                risk_score,
                risk_level,
                photo_name,
                audio_name,
                "NEW",
                created_at
            )
        )

        connection.commit()

    except sqlite3.IntegrityError as error:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": (
                "Unable to create the health report."
            ),
            "error": str(error)
        }), 500

    finally:

        connection.close()

    # --------------------------------------------------------
    # REPORT OBJECT
    # --------------------------------------------------------

    report = {
        "report_id": report_id,
        "username": username,
        "animal_name": animal_name,
        "species": species,
        "severity": severity,
        "symptoms": symptoms_text,
        "description": description,
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "photo_name": photo_name,
        "audio_name": audio_name,
        "status": "NEW",
        "created_at": created_at
    }

    # --------------------------------------------------------
    # NOTIFICATION
    # --------------------------------------------------------

    try:

        notify_for_report(report)

    except Exception as error:

        print(
            "Notification creation error:",
            error
        )

    # --------------------------------------------------------
    # CLUSTER CHECK
    # --------------------------------------------------------

    cluster_notification_created = False

    try:

        if location:

            clusters = build_location_clusters(
                days=14,
                minimum_reports=2
            )

            matching_cluster = None

            for cluster in clusters:

                cluster_location = str(
                    cluster.get("location")
                    or ""
                ).strip().lower()

                if cluster_location == location.lower():

                    matching_cluster = cluster
                    break

            if matching_cluster:

                from services.notification_service import (
                    notify_for_cluster
                )

                notification_id = notify_for_cluster(
                    matching_cluster
                )

                if notification_id:
                    cluster_notification_created = True

    except Exception as error:

        print(
            "Cluster notification error:",
            error
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return jsonify({

        "success": True,

        "message":
            "Health report submitted successfully.",

        "report":
            report,

        "notificationsCreated":
            True,

        "clusterNotificationCreated":
            cluster_notification_created

    }), 201


# ============================================================
# GET ALL HEALTH REPORTS
# ============================================================

@health_reports_bp.route(
    "",
    methods=["GET"]
)
@jwt_required()
def get_health_reports():

    ensure_health_reports_table()

    user = get_current_user_data()

    username = user["username"]

    role = user["role"]

    privileged_roles = {
        "VETERINARIAN",
        "LAB_STAFF",
        "DISTRICT_OFFICER",
        "STATE_ADMIN",
        "SUPER_ADMIN"
    }

    connection = get_connection()

    try:

        cursor = connection.cursor()

        if role in privileged_roles:

            cursor.execute(
                """
                SELECT
                    id,
                    report_id,
                    username,
                    animal_name,
                    species,
                    severity,
                    symptoms,
                    description,
                    location,
                    latitude,
                    longitude,
                    risk_score,
                    risk_level,
                    photo_name,
                    audio_name,
                    status,
                    created_at
                FROM health_reports
                ORDER BY id DESC
                """
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    report_id,
                    username,
                    animal_name,
                    species,
                    severity,
                    symptoms,
                    description,
                    location,
                    latitude,
                    longitude,
                    risk_score,
                    risk_level,
                    photo_name,
                    audio_name,
                    status,
                    created_at
                FROM health_reports
                WHERE username = ?
                ORDER BY id DESC
                """,
                (
                    username,
                )
            )

        rows = cursor.fetchall()

        reports = [
            dict(row)
            for row in rows
        ]

        return jsonify({

            "success": True,

            "reports": reports,

            "count": len(reports)

        })

    finally:

        connection.close()


# ============================================================
# GET SINGLE REPORT
# ============================================================

@health_reports_bp.route(
    "/<report_id>",
    methods=["GET"]
)
@jwt_required()
def get_health_report(report_id):

    ensure_health_reports_table()

    user = get_current_user_data()

    username = user["username"]

    role = user["role"]

    privileged_roles = {
        "VETERINARIAN",
        "LAB_STAFF",
        "DISTRICT_OFFICER",
        "STATE_ADMIN",
        "SUPER_ADMIN"
    }

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                report_id,
                username,
                animal_name,
                species,
                severity,
                symptoms,
                description,
                location,
                latitude,
                longitude,
                risk_score,
                risk_level,
                photo_name,
                audio_name,
                status,
                created_at
            FROM health_reports
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
                "message": "Health report not found."
            }), 404

        if (
            role not in privileged_roles
            and row["username"] != username
        ):

            return jsonify({
                "success": False,
                "message": (
                    "You do not have permission "
                    "to view this report."
                )
            }), 403

        return jsonify({

            "success": True,

            "report": dict(row)

        })

    finally:

        connection.close()


# ============================================================
# UPDATE REPORT STATUS
# ============================================================

@health_reports_bp.route(
    "/<report_id>/status",
    methods=["PUT"]
)
@role_required(
    "VETERINARIAN",
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN"
)
def update_report_status(report_id):

    ensure_health_reports_table()

    data = request.get_json(
        silent=True
    ) or {}

    status = str(
        data.get("status")
        or ""
    ).strip().upper()

    allowed_statuses = {
        "NEW",
        "UNDER INVESTIGATION",
        "SENT TO LAB",
        "VALIDATED",
        "SENT TO SURVEILLANCE",
        "RESOLVED",
        "REJECTED"
    }

    if status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": "Invalid report status."
        }), 400

    connection = get_connection()

    try:

        cursor = connection.cursor()

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

        if cursor.rowcount == 0:

            connection.rollback()

            return jsonify({
                "success": False,
                "message": "Health report not found."
            }), 404

        connection.commit()

        cursor.execute(
            """
            SELECT
                id,
                report_id,
                username,
                animal_name,
                species,
                severity,
                symptoms,
                description,
                location,
                latitude,
                longitude,
                risk_score,
                risk_level,
                photo_name,
                audio_name,
                status,
                created_at
            FROM health_reports
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
                "Report status updated successfully.",

            "report":
                dict(row)

        })

    finally:

        connection.close()


# ============================================================
# MODULE STATUS
# ============================================================

@health_reports_bp.route(
    "/status",
    methods=["GET"]
)
@jwt_required()
def health_reports_status():

    ensure_health_reports_table()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM health_reports
            """
        )

        row = cursor.fetchone()

        report_count = int(
            row[0] or 0
        )

    finally:

        connection.close()

    return jsonify({

        "success": True,

        "module":
            "Health Reports",

        "status":
            "active",

        "reportCount":
            report_count

    })