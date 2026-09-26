import os
import sqlite3
from datetime import datetime, timedelta


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
# DATABASE
# ============================================================

def get_connection():
    os.makedirs(
        os.path.dirname(DB_PATH),
        exist_ok=True
    )

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def ensure_notifications_table():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_username TEXT,
                recipient_role TEXT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT DEFAULT 'GENERAL',
                related_report_id TEXT,
                related_location TEXT,
                priority TEXT DEFAULT 'NORMAL',
                is_read INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )

        # Safe migration for databases created by the previous version
        columns = connection.execute(
            "PRAGMA table_info(notifications)"
        ).fetchall()

        column_names = {
            row["name"]
            for row in columns
        }

        if "related_location" not in column_names:
            connection.execute(
                """
                ALTER TABLE notifications
                ADD COLUMN related_location TEXT
                """
            )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# DUPLICATE CHECK
# ============================================================

def notification_exists(
    notification_type,
    related_report_id=None,
    related_location=None,
    recipient_role=None,
    hours=24
):
    ensure_notifications_table()

    connection = get_connection()

    try:
        cutoff = datetime.now() - timedelta(
            hours=hours
        )

        conditions = [
            "notification_type = ?",
            "created_at >= ?"
        ]

        params = [
            notification_type,
            cutoff.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ]

        if related_report_id is not None:
            conditions.append(
                "related_report_id = ?"
            )
            params.append(
                related_report_id
            )

        if related_location is not None:
            conditions.append(
                "related_location = ?"
            )
            params.append(
                related_location
            )

        if recipient_role is not None:
            conditions.append(
                "recipient_role = ?"
            )
            params.append(
                recipient_role
            )

        query = f"""
            SELECT id
            FROM notifications
            WHERE {" AND ".join(conditions)}
            LIMIT 1
        """

        cursor = connection.cursor()

        cursor.execute(
            query,
            tuple(params)
        )

        return cursor.fetchone() is not None

    finally:
        connection.close()


# ============================================================
# CREATE NOTIFICATION
# ============================================================

def create_notification(
    title,
    message,
    notification_type="GENERAL",
    related_report_id=None,
    related_location=None,
    priority="NORMAL",
    recipient_username=None,
    recipient_role=None
):
    ensure_notifications_table()

    connection = get_connection()

    try:
        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO notifications (
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
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
            """,
            (
                recipient_username,
                recipient_role,
                title,
                message,
                notification_type,
                related_report_id,
                related_location,
                priority,
                created_at
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


# ============================================================
# ROLE NOTIFICATION
# ============================================================

def notify_role(
    role,
    title,
    message,
    notification_type="GENERAL",
    related_report_id=None,
    related_location=None,
    priority="NORMAL"
):
    return create_notification(
        title=title,
        message=message,
        notification_type=notification_type,
        related_report_id=related_report_id,
        related_location=related_location,
        priority=priority,
        recipient_role=role
    )


# ============================================================
# REPORT-BASED NOTIFICATION
# ============================================================

def notify_for_report(report):
    """
    Creates role-based notifications from a new health report.

    HIGH:
        Veterinarian + District Officer

    MEDIUM:
        Veterinarian

    LOW:
        No priority alert is generated.
    """

    ensure_notifications_table()

    if not report:
        return []

    report_id = (
        report.get("report_id")
        or report.get("reportId")
    )

    animal_name = (
        report.get("animal_name")
        or report.get("animalName")
        or "Unknown animal"
    )

    location = (
        report.get("location")
        or "Unknown location"
    )

    risk_level = str(
        report.get("risk_level")
        or report.get("riskLevel")
        or ""
    ).upper()

    risk_score = (
        report.get("risk_score")
        if report.get("risk_score") is not None
        else report.get("riskScore", 0)
    )

    notifications = []

    # --------------------------------------------------------
    # HIGH RISK
    # --------------------------------------------------------

    if risk_level == "HIGH":

        vet_exists = notification_exists(
            notification_type="HIGH_RISK_REPORT",
            related_report_id=report_id,
            recipient_role="VETERINARIAN",
            hours=24
        )

        if not vet_exists:

            notification_id = create_notification(
                title="High-Risk Livestock Report",
                message=(
                    f"{animal_name} at {location} has an "
                    f"AI-assisted high-risk signal "
                    f"(score {risk_score}). "
                    f"Veterinary review is required."
                ),
                notification_type="HIGH_RISK_REPORT",
                related_report_id=report_id,
                related_location=location,
                priority="HIGH",
                recipient_role="VETERINARIAN"
            )

            notifications.append(
                notification_id
            )

        officer_exists = notification_exists(
            notification_type="HIGH_RISK_REPORT",
            related_report_id=report_id,
            recipient_role="DISTRICT_OFFICER",
            hours=24
        )

        if not officer_exists:

            notification_id = create_notification(
                title="High-Risk Surveillance Signal",
                message=(
                    f"High-risk field signal reported for "
                    f"{animal_name} at {location}. "
                    f"Report {report_id} requires surveillance review."
                ),
                notification_type="HIGH_RISK_REPORT",
                related_report_id=report_id,
                related_location=location,
                priority="HIGH",
                recipient_role="DISTRICT_OFFICER"
            )

            notifications.append(
                notification_id
            )

    # --------------------------------------------------------
    # MEDIUM RISK
    # --------------------------------------------------------

    elif risk_level == "MEDIUM":

        exists = notification_exists(
            notification_type="MEDIUM_RISK_REPORT",
            related_report_id=report_id,
            recipient_role="VETERINARIAN",
            hours=24
        )

        if not exists:

            notification_id = create_notification(
                title="Medium-Risk Livestock Report",
                message=(
                    f"{animal_name} at {location} has an "
                    f"AI-assisted medium-risk signal "
                    f"(score {risk_score}). "
                    f"Veterinary triage is recommended."
                ),
                notification_type="MEDIUM_RISK_REPORT",
                related_report_id=report_id,
                related_location=location,
                priority="MEDIUM",
                recipient_role="VETERINARIAN"
            )

            notifications.append(
                notification_id
            )

    return notifications


# ============================================================
# CLUSTER NOTIFICATION
# ============================================================

def notify_for_cluster(cluster):
    """
    Creates one notification for a newly observed
    potential emerging cluster.

    Duplicate cluster notifications for the same
    location are suppressed for 24 hours.
    """

    ensure_notifications_table()

    if not cluster:
        return None

    if not cluster.get(
        "potentialEmergingCluster"
    ):
        return None

    location = (
        cluster.get("location")
        or "Unknown location"
    )

    score = cluster.get(
        "clusterScore",
        0
    )

    report_count = cluster.get(
        "reportCount",
        0
    )

    priority = str(
        cluster.get("priority")
        or "WATCH"
    ).upper()

    if notification_exists(
        notification_type="POTENTIAL_CLUSTER",
        related_location=location,
        recipient_role="DISTRICT_OFFICER",
        hours=24
    ):
        return None

    return create_notification(
        title="Potential Emerging Cluster",
        message=(
            f"A potential livestock-health reporting "
            f"cluster has been identified around {location}. "
            f"Cluster signal score: {score}/100. "
            f"Reports included: {report_count}. "
            f"Human veterinary and epidemiological "
            f"review is required."
        ),
        notification_type="POTENTIAL_CLUSTER",
        related_location=location,
        priority=(
            "HIGH"
            if priority == "HIGH PRIORITY"
            else "MEDIUM"
        ),
        recipient_role="DISTRICT_OFFICER"
    )


# ============================================================
# GET USER NOTIFICATIONS
# ============================================================

def get_user_notifications(
    username=None,
    role=None,
    unread_only=False,
    limit=50
):
    ensure_notifications_table()

    connection = get_connection()

    try:
        conditions = []
        params = []

        if username:
            conditions.append(
                """
                (
                    recipient_username = ?
                    OR recipient_username IS NULL
                )
                """
            )

            params.append(
                username
            )

        if role:
            conditions.append(
                """
                (
                    recipient_role = ?
                    OR recipient_role IS NULL
                )
                """
            )

            params.append(
                role
            )

        if unread_only:
            conditions.append(
                "is_read = 0"
            )

        where_clause = ""

        if conditions:
            where_clause = (
                "WHERE " +
                " AND ".join(
                    conditions
                )
            )

        try:
            limit = int(
                limit
            )
        except (
            TypeError,
            ValueError
        ):
            limit = 50

        limit = max(
            1,
            min(limit, 100)
        )

        query = f"""
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
            {where_clause}
            ORDER BY id DESC
            LIMIT ?
        """

        params.append(
            limit
        )

        cursor = connection.cursor()

        cursor.execute(
            query,
            tuple(params)
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()


# ============================================================
# UNREAD COUNT
# ============================================================

def get_unread_count(
    username=None,
    role=None
):
    ensure_notifications_table()

    connection = get_connection()

    try:
        conditions = [
            "is_read = 0"
        ]

        params = []

        if username:
            conditions.append(
                """
                (
                    recipient_username = ?
                    OR recipient_username IS NULL
                )
                """
            )

            params.append(
                username
            )

        if role:
            conditions.append(
                """
                (
                    recipient_role = ?
                    OR recipient_role IS NULL
                )
                """
            )

            params.append(
                role
            )

        query = f"""
            SELECT COUNT(*)
            FROM notifications
            WHERE {" AND ".join(conditions)}
        """

        cursor = connection.cursor()

        cursor.execute(
            query,
            tuple(params)
        )

        row = cursor.fetchone()

        return int(
            row[0] or 0
        )

    finally:
        connection.close()


# ============================================================
# MARK ONE AS READ
# ============================================================

def mark_notification_read(
    notification_id
):
    ensure_notifications_table()

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE notifications
            SET is_read = 1
            WHERE id = ?
            """,
            (
                notification_id,
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# ============================================================
# MARK ALL AS READ
# ============================================================

def mark_all_read(
    username=None,
    role=None
):
    ensure_notifications_table()

    connection = get_connection()

    try:
        conditions = []
        params = []

        if username:
            conditions.append(
                """
                (
                    recipient_username = ?
                    OR recipient_username IS NULL
                )
                """
            )

            params.append(
                username
            )

        if role:
            conditions.append(
                """
                (
                    recipient_role = ?
                    OR recipient_role IS NULL
                )
                """
            )

            params.append(
                role
            )

        if conditions:
            where_clause = (
                "WHERE " +
                " AND ".join(
                    conditions
                ) +
                " AND is_read = 0"
            )
        else:
            where_clause = (
                "WHERE is_read = 0"
            )

        cursor = connection.cursor()

        cursor.execute(
            f"""
            UPDATE notifications
            SET is_read = 1
            {where_clause}
            """,
            tuple(params)
        )

        connection.commit()

        return cursor.rowcount

    finally:
        connection.close()