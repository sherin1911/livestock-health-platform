from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from utils.authorization import role_required

import os
import sqlite3


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "instance", "database.db")


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def table_exists(connection, table_name):
    cursor = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    )

    row = cursor.fetchone()
    return row is not None


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
@role_required(
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN",
)
def dashboard_summary():
    connection = get_db_connection()

    try:
        if not table_exists(connection, "health_reports"):
            return jsonify(
                {
                    "success": True,
                    "summary": {
                        "monitoredAnimals": 0,
                        "totalReports": 0,
                        "activeAlerts": 0,
                        "highRiskCases": 0,
                        "mediumRiskCases": 0,
                        "lowRiskCases": 0,
                        "validatedCases": 0,
                        "underInvestigation": 0,
                        "sentToLaboratory": 0,
                        "sentToSurveillance": 0,
                    },
                }
            ), 200

        total_reports = connection.execute(
            "SELECT COUNT(*) AS count FROM health_reports"
        ).fetchone()["count"]

        monitored_animals = connection.execute(
            """
            SELECT COUNT(DISTINCT
                CASE
                    WHEN animal_name IS NOT NULL
                    AND TRIM(animal_name) != ''
                    THEN animal_name
                END
            ) AS count
            FROM health_reports
            """
        ).fetchone()["count"]

        high_risk = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM health_reports
            WHERE UPPER(COALESCE(risk_level, severity, '')) = 'HIGH'
            """
        ).fetchone()["count"]

        medium_risk = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM health_reports
            WHERE UPPER(COALESCE(risk_level, severity, '')) = 'MEDIUM'
            """
        ).fetchone()["count"]

        low_risk = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM health_reports
            WHERE UPPER(COALESCE(risk_level, severity, '')) = 'LOW'
            """
        ).fetchone()["count"]

        validated_cases = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM health_reports
            WHERE UPPER(COALESCE(status, '')) = 'VALIDATED'
            """
        ).fetchone()["count"]

        under_investigation = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM health_reports
            WHERE UPPER(COALESCE(status, '')) = 'UNDER INVESTIGATION'
            """
        ).fetchone()["count"]

        sent_to_laboratory = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM health_reports
            WHERE UPPER(COALESCE(status, '')) = 'SENT TO LAB'
            """
        ).fetchone()["count"]

        sent_to_surveillance = 0

        if table_exists(connection, "laboratory_records"):
            sent_to_surveillance = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM laboratory_records
                WHERE sent_to_surveillance = 1
                """
            ).fetchone()["count"]

        active_alerts = 0

        if table_exists(connection, "notifications"):
            active_alerts = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM notifications
                WHERE is_read = 0
                AND recipient_role IN (
                    'DISTRICT_OFFICER',
                    'STATE_ADMIN',
                    'SUPER_ADMIN'
                )
                """
            ).fetchone()["count"]

        summary = {
            "monitoredAnimals": monitored_animals,
            "totalReports": total_reports,
            "activeAlerts": active_alerts,
            "highRiskCases": high_risk,
            "mediumRiskCases": medium_risk,
            "lowRiskCases": low_risk,
            "validatedCases": validated_cases,
            "underInvestigation": under_investigation,
            "sentToLaboratory": sent_to_laboratory,
            "sentToSurveillance": sent_to_surveillance,
        }

        return jsonify(
            {
                "success": True,
                "summary": summary,
            }
        ), 200

    except sqlite3.Error as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load dashboard summary.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# RISK DISTRIBUTION
# ============================================================

@dashboard_bp.route("/risk-distribution", methods=["GET"])
@jwt_required()
@role_required(
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN",
)
def risk_distribution():
    connection = get_db_connection()

    try:
        distribution = {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        if not table_exists(connection, "health_reports"):
            return jsonify(
                {
                    "success": True,
                    "distribution": distribution,
                }
            ), 200

        rows = connection.execute(
            """
            SELECT
                UPPER(COALESCE(risk_level, severity, 'LOW')) AS risk,
                COUNT(*) AS count
            FROM health_reports
            GROUP BY UPPER(COALESCE(risk_level, severity, 'LOW'))
            """
        ).fetchall()

        for row in rows:
            risk = row["risk"]

            if risk in distribution:
                distribution[risk] = row["count"]

        return jsonify(
            {
                "success": True,
                "distribution": distribution,
            }
        ), 200

    except sqlite3.Error as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load risk distribution.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# DISTRICT / LOCATION SUMMARY
# ============================================================

@dashboard_bp.route("/districts", methods=["GET"])
@jwt_required()
@role_required(
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN",
)
def district_summary():
    connection = get_db_connection()

    try:
        if not table_exists(connection, "health_reports"):
            return jsonify(
                {
                    "success": True,
                    "districts": [],
                }
            ), 200

        rows = connection.execute(
            """
            SELECT
                COALESCE(NULLIF(TRIM(location), ''), 'Unknown Location') AS location,
                COUNT(*) AS totalReports,
                SUM(
                    CASE
                        WHEN UPPER(COALESCE(risk_level, severity, '')) = 'HIGH'
                        THEN 1 ELSE 0
                    END
                ) AS highRisk,
                SUM(
                    CASE
                        WHEN UPPER(COALESCE(risk_level, severity, '')) = 'MEDIUM'
                        THEN 1 ELSE 0
                    END
                ) AS mediumRisk,
                SUM(
                    CASE
                        WHEN UPPER(COALESCE(risk_level, severity, '')) = 'LOW'
                        THEN 1 ELSE 0
                    END
                ) AS lowRisk
            FROM health_reports
            GROUP BY COALESCE(NULLIF(TRIM(location), ''), 'Unknown Location')
            ORDER BY totalReports DESC
            """
        ).fetchall()

        districts = []

        for row in rows:
            districts.append(
                {
                    "district": row["location"],
                    "location": row["location"],
                    "totalReports": row["totalReports"] or 0,
                    "highRisk": row["highRisk"] or 0,
                    "mediumRisk": row["mediumRisk"] or 0,
                    "lowRisk": row["lowRisk"] or 0,
                }
            )

        return jsonify(
            {
                "success": True,
                "districts": districts,
            }
        ), 200

    except sqlite3.Error as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load district information.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# RECENT REPORTS
# ============================================================

@dashboard_bp.route("/recent-reports", methods=["GET"])
@jwt_required()
@role_required(
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN",
)
def recent_reports():
    connection = get_db_connection()

    try:
        if not table_exists(connection, "health_reports"):
            return jsonify(
                {
                    "success": True,
                    "reports": [],
                }
            ), 200

        rows = connection.execute(
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
            LIMIT 20
            """
        ).fetchall()

        reports = []

        for row in rows:
            reports.append(
                {
                    "id": row["id"],
                    "reportId": row["report_id"],
                    "username": row["username"],
                    "animalName": row["animal_name"],
                    "species": row["species"],
                    "severity": row["severity"],
                    "symptoms": row["symptoms"],
                    "description": row["description"],
                    "location": row["location"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "riskScore": row["risk_score"],
                    "riskLevel": row["risk_level"],
                    "photoName": row["photo_name"],
                    "audioName": row["audio_name"],
                    "status": row["status"],
                    "createdAt": row["created_at"],
                }
            )

        return jsonify(
            {
                "success": True,
                "reports": reports,
            }
        ), 200

    except sqlite3.Error as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load recent reports.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# ACTIVE ALERTS
# ============================================================

@dashboard_bp.route("/alerts", methods=["GET"])
@jwt_required()
@role_required(
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN",
)
def dashboard_alerts():
    connection = get_db_connection()

    try:
        alerts = []

        if table_exists(connection, "notifications"):
            rows = connection.execute(
                """
                SELECT
                    id,
                    recipient_username,
                    recipient_role,
                    title,
                    message,
                    notification_type,
                    related_report_id,
                    related_location,
                    priority,
                    is_read,
                    created_at
                FROM notifications
                WHERE recipient_role IN (
                    'DISTRICT_OFFICER',
                    'STATE_ADMIN',
                    'SUPER_ADMIN'
                )
                ORDER BY
                    CASE
                        WHEN UPPER(COALESCE(priority, 'LOW')) = 'HIGH' THEN 1
                        WHEN UPPER(COALESCE(priority, 'LOW')) = 'MEDIUM' THEN 2
                        ELSE 3
                    END,
                    id DESC
                LIMIT 30
                """
            ).fetchall()

            for row in rows:
                alerts.append(
                    {
                        "id": row["id"],
                        "recipientUsername": row["recipient_username"],
                        "recipientRole": row["recipient_role"],
                        "title": row["title"],
                        "message": row["message"],
                        "notificationType": row["notification_type"],
                        "relatedReportId": row["related_report_id"],
                        "relatedLocation": row["related_location"],
                        "priority": row["priority"],
                        "isRead": bool(row["is_read"]),
                        "createdAt": row["created_at"],
                    }
                )

        return jsonify(
            {
                "success": True,
                "alerts": alerts,
            }
        ), 200

    except sqlite3.Error as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load alerts.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# COMPLETE GOVERNMENT OVERVIEW
# ============================================================

@dashboard_bp.route("/overview", methods=["GET"])
@jwt_required()
@role_required(
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN",
)
def dashboard_overview():
    connection = get_db_connection()

    try:
        summary = {
            "monitoredAnimals": 0,
            "totalReports": 0,
            "activeAlerts": 0,
            "highRiskCases": 0,
            "mediumRiskCases": 0,
            "lowRiskCases": 0,
            "validatedCases": 0,
            "underInvestigation": 0,
            "sentToLaboratory": 0,
            "sentToSurveillance": 0,
        }

        distribution = {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        districts = []
        reports = []
        alerts = []

        if table_exists(connection, "health_reports"):
            summary["totalReports"] = connection.execute(
                "SELECT COUNT(*) AS count FROM health_reports"
            ).fetchone()["count"]

            summary["monitoredAnimals"] = connection.execute(
                """
                SELECT COUNT(DISTINCT
                    CASE
                        WHEN animal_name IS NOT NULL
                        AND TRIM(animal_name) != ''
                        THEN animal_name
                    END
                ) AS count
                FROM health_reports
                """
            ).fetchone()["count"]

            summary["highRiskCases"] = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM health_reports
                WHERE UPPER(COALESCE(risk_level, severity, '')) = 'HIGH'
                """
            ).fetchone()["count"]

            summary["mediumRiskCases"] = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM health_reports
                WHERE UPPER(COALESCE(risk_level, severity, '')) = 'MEDIUM'
                """
            ).fetchone()["count"]

            summary["lowRiskCases"] = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM health_reports
                WHERE UPPER(COALESCE(risk_level, severity, '')) = 'LOW'
                """
            ).fetchone()["count"]

            summary["validatedCases"] = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM health_reports
                WHERE UPPER(COALESCE(status, '')) = 'VALIDATED'
                """
            ).fetchone()["count"]

            summary["underInvestigation"] = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM health_reports
                WHERE UPPER(COALESCE(status, '')) = 'UNDER INVESTIGATION'
                """
            ).fetchone()["count"]

            summary["sentToLaboratory"] = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM health_reports
                WHERE UPPER(COALESCE(status, '')) = 'SENT TO LAB'
                """
            ).fetchone()["count"]

            risk_rows = connection.execute(
                """
                SELECT
                    UPPER(COALESCE(risk_level, severity, 'LOW')) AS risk,
                    COUNT(*) AS count
                FROM health_reports
                GROUP BY UPPER(COALESCE(risk_level, severity, 'LOW'))
                """
            ).fetchall()

            for row in risk_rows:
                if row["risk"] in distribution:
                    distribution[row["risk"]] = row["count"]

            district_rows = connection.execute(
                """
                SELECT
                    COALESCE(NULLIF(TRIM(location), ''), 'Unknown Location') AS location,
                    COUNT(*) AS totalReports,
                    SUM(
                        CASE
                            WHEN UPPER(
                                COALESCE(risk_level, severity, '')
                            ) = 'HIGH'
                            THEN 1 ELSE 0
                        END
                    ) AS highRisk,
                    SUM(
                        CASE
                            WHEN UPPER(
                                COALESCE(risk_level, severity, '')
                            ) = 'MEDIUM'
                            THEN 1 ELSE 0
                        END
                    ) AS mediumRisk,
                    SUM(
                        CASE
                            WHEN UPPER(
                                COALESCE(risk_level, severity, '')
                            ) = 'LOW'
                            THEN 1 ELSE 0
                        END
                    ) AS lowRisk
                FROM health_reports
                GROUP BY COALESCE(
                    NULLIF(TRIM(location), ''),
                    'Unknown Location'
                )
                ORDER BY totalReports DESC
                """
            ).fetchall()

            for row in district_rows:
                districts.append(
                    {
                        "district": row["location"],
                        "location": row["location"],
                        "totalReports": row["totalReports"] or 0,
                        "highRisk": row["highRisk"] or 0,
                        "mediumRisk": row["mediumRisk"] or 0,
                        "lowRisk": row["lowRisk"] or 0,
                    }
                )

            report_rows = connection.execute(
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
                LIMIT 20
                """
            ).fetchall()

            for row in report_rows:
                reports.append(
                    {
                        "id": row["id"],
                        "reportId": row["report_id"],
                        "username": row["username"],
                        "animalName": row["animal_name"],
                        "species": row["species"],
                        "severity": row["severity"],
                        "symptoms": row["symptoms"],
                        "description": row["description"],
                        "location": row["location"],
                        "latitude": row["latitude"],
                        "longitude": row["longitude"],
                        "riskScore": row["risk_score"],
                        "riskLevel": row["risk_level"],
                        "photoName": row["photo_name"],
                        "audioName": row["audio_name"],
                        "status": row["status"],
                        "createdAt": row["created_at"],
                    }
                )

        if table_exists(connection, "laboratory_records"):
            summary["sentToSurveillance"] = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM laboratory_records
                WHERE sent_to_surveillance = 1
                """
            ).fetchone()["count"]

        if table_exists(connection, "notifications"):
            summary["activeAlerts"] = connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM notifications
                WHERE is_read = 0
                AND recipient_role IN (
                    'DISTRICT_OFFICER',
                    'STATE_ADMIN',
                    'SUPER_ADMIN'
                )
                """
            ).fetchone()["count"]

            alert_rows = connection.execute(
                """
                SELECT
                    id,
                    recipient_username,
                    recipient_role,
                    title,
                    message,
                    notification_type,
                    related_report_id,
                    related_location,
                    priority,
                    is_read,
                    created_at
                FROM notifications
                WHERE recipient_role IN (
                    'DISTRICT_OFFICER',
                    'STATE_ADMIN',
                    'SUPER_ADMIN'
                )
                ORDER BY
                    CASE
                        WHEN UPPER(COALESCE(priority, 'LOW')) = 'HIGH'
                        THEN 1
                        WHEN UPPER(COALESCE(priority, 'LOW')) = 'MEDIUM'
                        THEN 2
                        ELSE 3
                    END,
                    id DESC
                LIMIT 30
                """
            ).fetchall()

            for row in alert_rows:
                alerts.append(
                    {
                        "id": row["id"],
                        "recipientUsername": row["recipient_username"],
                        "recipientRole": row["recipient_role"],
                        "title": row["title"],
                        "message": row["message"],
                        "notificationType": row["notification_type"],
                        "relatedReportId": row["related_report_id"],
                        "relatedLocation": row["related_location"],
                        "priority": row["priority"],
                        "isRead": bool(row["is_read"]),
                        "createdAt": row["created_at"],
                    }
                )

        return jsonify(
            {
                "success": True,
                "summary": summary,
                "riskDistribution": distribution,
                "districts": districts,
                "recentReports": reports,
                "alerts": alerts,
            }
        ), 200

    except sqlite3.Error as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load government dashboard.",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()


# ============================================================
# DASHBOARD STATUS
# ============================================================

@dashboard_bp.route("/status", methods=["GET"])
@jwt_required()
@role_required(
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN",
)
def dashboard_status():
    connection = get_db_connection()

    try:
        health_reports_ready = table_exists(
            connection,
            "health_reports",
        )

        investigations_ready = table_exists(
            connection,
            "investigations",
        )

        laboratory_ready = table_exists(
            connection,
            "laboratory_records",
        )

        notifications_ready = table_exists(
            connection,
            "notifications",
        )

        return jsonify(
            {
                "success": True,
                "status": "operational",
                "database": "connected",
                "modules": {
                    "healthReports": health_reports_ready,
                    "investigations": investigations_ready,
                    "laboratory": laboratory_ready,
                    "notifications": notifications_ready,
                },
            }
        ), 200

    except sqlite3.Error as error:
        return jsonify(
            {
                "success": False,
                "status": "degraded",
                "database": "error",
                "error": str(error),
            }
        ), 500

    finally:
        connection.close()