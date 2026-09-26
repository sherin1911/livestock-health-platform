from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

import sqlite3
import os
from datetime import datetime

from utils.authorization import role_required


# ============================================================
# BLUEPRINT
# ============================================================

laboratory_bp = Blueprint(
    "laboratory",
    __name__,
    url_prefix="/api/laboratory"
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
# CREATE LABORATORY TABLE
# ============================================================

def ensure_laboratory_table():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS laboratory_records (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                report_id TEXT UNIQUE NOT NULL,

                laboratory_username TEXT,

                sample_id TEXT,

                sample_type TEXT,

                test_type TEXT,

                result TEXT,

                assay_reference TEXT,

                findings TEXT,

                surveillance_classification TEXT,

                sent_to_surveillance INTEGER DEFAULT 0,

                validation_date TEXT,

                created_at TEXT NOT NULL,

                updated_at TEXT NOT NULL

            )
            """
        )

        connection.commit()

    finally:

        connection.close()


# ============================================================
# CREATE HEALTH REPORT TABLE IF NEEDED
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
# CREATE INVESTIGATION TABLE IF NEEDED
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
# CURRENT USER
# ============================================================

def get_current_user():

    identity = get_jwt_identity()

    if isinstance(
        identity,
        dict
    ):

        return {
            "user_id":
                identity.get("user_id"),

            "username":
                identity.get("username"),

            "role":
                str(
                    identity.get("role")
                    or ""
                ).upper()
        }

    return {
        "user_id":
            None,

        "username":
            identity,

        "role":
            ""
    }


# ============================================================
# NORMALIZE VALUE
# ============================================================

def clean_value(value):

    if value is None:
        return ""

    return str(
        value
    ).strip()


# ============================================================
# VALIDATE RESULT
# ============================================================

ALLOWED_RESULTS = {
    "NEGATIVE",
    "POSITIVE",
    "INCONCLUSIVE"
}


def normalize_result(value):

    result = str(
        value or ""
    ).strip().upper()

    if result not in ALLOWED_RESULTS:
        return None

    return result


# ============================================================
# VALIDATE SAMPLE
# ============================================================

ALLOWED_SAMPLE_TYPES = {
    "Milk",
    "Blood",
    "Serum",
    "Swab",
    "Stool",
    "Urine",
    "Tissue"
}


def validate_sample_type(value):

    value = clean_value(value)

    if not value:
        return False

    return value in ALLOWED_SAMPLE_TYPES


# ============================================================
# VALIDATE TEST
# ============================================================

ALLOWED_TEST_TYPES = {
    "Microscopic Examination",
    "Culture/Isolation",
    "PCR/Molecular Test",
    "Serological Test",
    "Rapid Diagnostic Test",
    "Milk Quality Analysis"
}


def validate_test_type(value):

    value = clean_value(value)

    if not value:
        return False

    return value in ALLOWED_TEST_TYPES


# ============================================================
# CALCULATE NEXT REPORT STATUS
# ============================================================

def get_report_status(
    result,
    sent_to_surveillance
):

    if sent_to_surveillance:

        return "SENT TO SURVEILLANCE"

    if result == "INCONCLUSIVE":

        return "UNDER INVESTIGATION"

    if result in {
        "POSITIVE",
        "NEGATIVE"
    }:

        return "VALIDATED"

    return "SENT TO LAB"


# ============================================================
# GET SINGLE LAB RECORD
# ============================================================

def fetch_laboratory_record(
    connection,
    report_id
):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            report_id,
            laboratory_username,
            sample_id,
            sample_type,
            test_type,
            result,
            assay_reference,
            findings,
            surveillance_classification,
            sent_to_surveillance,
            validation_date,
            created_at,
            updated_at
        FROM laboratory_records
        WHERE report_id = ?
        LIMIT 1
        """,
        (
            report_id,
        )
    )

    row = cursor.fetchone()

    if not row:
        return None

    return dict(row)


# ============================================================
# CREATE / UPDATE LABORATORY RECORD
# ============================================================

@laboratory_bp.route(
    "",
    methods=["POST"]
)
@role_required(
    "LAB_STAFF"
)
def save_laboratory_record():

    ensure_laboratory_table()
    ensure_health_reports_table()
    ensure_investigations_table()

    data = request.get_json(
        silent=True
    ) or {}

    user = get_current_user()

    laboratory_username = (
        user.get("username")
    )

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    report_id = clean_value(
        data.get("reportId")
        or data.get("report_id")
    )

    sample_id = clean_value(
        data.get("sampleId")
        or data.get("sample_id")
    )

    sample_type = clean_value(
        data.get("sampleType")
        or data.get("sample_type")
    )

    test_type = clean_value(
        data.get("testType")
        or data.get("test_type")
    )

    result = normalize_result(
        data.get("result")
    )

    assay_reference = clean_value(
        data.get("assayReference")
        or data.get("assay_reference")
    )

    findings = clean_value(
        data.get("findings")
    )

    surveillance_classification = clean_value(
        data.get("surveillanceClassification")
        or data.get("surveillance_classification")
    )

    sent_to_surveillance = data.get(
        "sentToSurveillance",
        data.get(
            "sent_to_surveillance",
            False
        )
    )

    validation_date = clean_value(
        data.get("validationDate")
        or data.get("validation_date")
    )

    # --------------------------------------------------------
    # NORMALIZE BOOLEAN
    # --------------------------------------------------------

    if isinstance(
        sent_to_surveillance,
        str
    ):

        sent_to_surveillance = (
            sent_to_surveillance.lower()
            in {
                "true",
                "1",
                "yes",
                "on"
            }
        )

    else:

        sent_to_surveillance = bool(
            sent_to_surveillance
        )

    sent_to_surveillance_value = (
        1
        if sent_to_surveillance
        else 0
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

    if not sample_id:

        return jsonify({
            "success": False,
            "message":
                "Sample ID is required."
        }), 400

    if not validate_sample_type(
        sample_type
    ):

        return jsonify({
            "success": False,
            "message":
                "Invalid sample type."
        }), 400

    if not validate_test_type(
        test_type
    ):

        return jsonify({
            "success": False,
            "message":
                "Invalid test type."
        }), 400

    if not result:

        return jsonify({
            "success": False,
            "message":
                "Laboratory result is required."
        }), 400

    if not validation_date:

        validation_date = datetime.now().strftime(
            "%Y-%m-%d"
        )

    # --------------------------------------------------------
    # CHECK REPORT EXISTS
    # --------------------------------------------------------

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                report_id,
                status
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
    # UPSERT
    # --------------------------------------------------------

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM laboratory_records
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
                UPDATE laboratory_records
                SET
                    laboratory_username = ?,
                    sample_id = ?,
                    sample_type = ?,
                    test_type = ?,
                    result = ?,
                    assay_reference = ?,
                    findings = ?,
                    surveillance_classification = ?,
                    sent_to_surveillance = ?,
                    validation_date = ?,
                    updated_at = ?
                WHERE report_id = ?
                """,
                (
                    laboratory_username,
                    sample_id,
                    sample_type,
                    test_type,
                    result,
                    assay_reference,
                    findings,
                    surveillance_classification,
                    sent_to_surveillance_value,
                    validation_date,
                    now,
                    report_id
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO laboratory_records (

                    report_id,
                    laboratory_username,
                    sample_id,
                    sample_type,
                    test_type,
                    result,
                    assay_reference,
                    findings,
                    surveillance_classification,
                    sent_to_surveillance,
                    validation_date,
                    created_at,
                    updated_at

                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?
                )
                """,
                (
                    report_id,
                    laboratory_username,
                    sample_id,
                    sample_type,
                    test_type,
                    result,
                    assay_reference,
                    findings,
                    surveillance_classification,
                    sent_to_surveillance_value,
                    validation_date,
                    now,
                    now
                )
            )

        # ----------------------------------------------------
        # UPDATE HEALTH REPORT
        # ----------------------------------------------------

        new_status = get_report_status(
            result,
            sent_to_surveillance
        )

        cursor.execute(
            """
            UPDATE health_reports
            SET status = ?
            WHERE report_id = ?
            """,
            (
                new_status,
                report_id
            )
        )

        # ----------------------------------------------------
        # UPDATE INVESTIGATION
        # ----------------------------------------------------

        investigation_status = (
            "VALIDATED"
            if result in {
                "POSITIVE",
                "NEGATIVE"
            }
            else "UNDER INVESTIGATION"
        )

        cursor.execute(
            """
            UPDATE investigations
            SET
                status = ?,
                updated_at = ?
            WHERE report_id = ?
            """,
            (
                investigation_status,
                now,
                report_id
            )
        )

        connection.commit()

        # ----------------------------------------------------
        # GET SAVED RECORD
        # ----------------------------------------------------

        laboratory = fetch_laboratory_record(
            connection,
            report_id
        )

    finally:

        connection.close()

    # --------------------------------------------------------
    # OPTIONAL SURVEILLANCE NOTIFICATION
    # --------------------------------------------------------

    if sent_to_surveillance:

        try:

            from services.notification_service import (
                create_notification
            )

            priority = (
                "HIGH"
                if result == "POSITIVE"
                else "MEDIUM"
            )

            create_notification(
                title="Laboratory Validation Submitted",
                message=(
                    f"Laboratory result {result} for "
                    f"report {report_id} has been submitted "
                    f"to surveillance review."
                ),
                notification_type="LAB_VALIDATION",
                related_report_id=report_id,
                priority=priority,
                recipient_role="DISTRICT_OFFICER"
            )

        except Exception as error:

            print(
                "Laboratory notification error:",
                error
            )

    return jsonify({

        "success":
            True,

        "message":
            (
                "Laboratory record saved successfully."
            ),

        "laboratory":
            laboratory

    }), 200


# ============================================================
# GET SINGLE LABORATORY RECORD
# ============================================================

@laboratory_bp.route(
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
def get_laboratory_record(
    report_id
):

    ensure_laboratory_table()

    report_id = clean_value(
        report_id
    )

    connection = get_connection()

    try:

        laboratory = fetch_laboratory_record(
            connection,
            report_id
        )

        if not laboratory:

            return jsonify({
                "success": False,
                "message":
                    "Laboratory record not found."
            }), 404

        return jsonify({

            "success":
                True,

            "laboratory":
                laboratory

        }), 200

    finally:

        connection.close()


# ============================================================
# GET ALL LABORATORY RECORDS
# ============================================================

@laboratory_bp.route(
    "",
    methods=["GET"]
)
@role_required(
    "LAB_STAFF",
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN"
)
def get_all_laboratory_records():

    ensure_laboratory_table()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT

                id,
                report_id,
                laboratory_username,
                sample_id,
                sample_type,
                test_type,
                result,
                assay_reference,
                findings,
                surveillance_classification,
                sent_to_surveillance,
                validation_date,
                created_at,
                updated_at

            FROM laboratory_records

            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        records = [
            dict(row)
            for row in rows
        ]

        return jsonify({

            "success":
                True,

            "laboratoryRecords":
                records,

            "count":
                len(records)

        }), 200

    finally:

        connection.close()


# ============================================================
# UPDATE LABORATORY RESULT
# ============================================================

@laboratory_bp.route(
    "/<report_id>/result",
    methods=["PUT"]
)
@role_required(
    "LAB_STAFF"
)
def update_laboratory_result(
    report_id
):

    ensure_laboratory_table()
    ensure_health_reports_table()

    data = request.get_json(
        silent=True
    ) or {}

    result = normalize_result(
        data.get("result")
    )

    findings = clean_value(
        data.get("findings")
    )

    surveillance_classification = clean_value(
        data.get("surveillanceClassification")
    )

    validation_date = clean_value(
        data.get("validationDate")
    )

    if not result:

        return jsonify({
            "success": False,
            "message":
                "Invalid laboratory result."
        }), 400

    if not validation_date:

        validation_date = datetime.now().strftime(
            "%Y-%m-%d"
        )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE laboratory_records

            SET
                result = ?,
                findings = ?,
                surveillance_classification = ?,
                validation_date = ?,
                updated_at = ?

            WHERE report_id = ?
            """,
            (
                result,
                findings,
                surveillance_classification,
                validation_date,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                report_id
            )
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return jsonify({
                "success": False,
                "message":
                    "Laboratory record not found."
            }), 404

        report_status = get_report_status(
            result,
            False
        )

        cursor.execute(
            """
            UPDATE health_reports

            SET status = ?

            WHERE report_id = ?
            """,
            (
                report_status,
                report_id
            )
        )

        connection.commit()

        laboratory = fetch_laboratory_record(
            connection,
            report_id
        )

    finally:

        connection.close()

    return jsonify({

        "success":
            True,

        "message":
            "Laboratory result updated.",

        "laboratory":
            laboratory

    }), 200


# ============================================================
# SEND TO SURVEILLANCE
# ============================================================

@laboratory_bp.route(
    "/<report_id>/surveillance",
    methods=["PUT"]
)
@role_required(
    "LAB_STAFF"
)
def send_to_surveillance(
    report_id
):

    ensure_laboratory_table()
    ensure_health_reports_table()
    ensure_investigations_table()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                result,
                surveillance_classification
            FROM laboratory_records
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
                    "Laboratory record not found."
            }), 404

        result = row["result"]

        if result not in ALLOWED_RESULTS:

            return jsonify({
                "success": False,
                "message":
                    "A valid laboratory result is required."
            }), 400

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            UPDATE laboratory_records

            SET
                sent_to_surveillance = 1,
                updated_at = ?

            WHERE report_id = ?
            """,
            (
                now,
                report_id
            )
        )

        cursor.execute(
            """
            UPDATE health_reports

            SET status = 'SENT TO SURVEILLANCE'

            WHERE report_id = ?
            """,
            (
                report_id,
            )
        )

        cursor.execute(
            """
            UPDATE investigations

            SET
                status = 'VALIDATED',
                surveillance_flag = 1,
                updated_at = ?

            WHERE report_id = ?
            """,
            (
                now,
                report_id
            )
        )

        connection.commit()

        laboratory = fetch_laboratory_record(
            connection,
            report_id
        )

    finally:

        connection.close()

    # --------------------------------------------------------
    # NOTIFY GOVERNMENT
    # --------------------------------------------------------

    try:

        from services.notification_service import (
            create_notification
        )

        priority = (
            "HIGH"
            if result == "POSITIVE"
            else "MEDIUM"
        )

        create_notification(
            title="Case Sent to Surveillance",
            message=(
                f"Laboratory-validated report "
                f"{report_id} has been forwarded "
                f"to surveillance review."
            ),
            notification_type="SURVEILLANCE_SUBMISSION",
            related_report_id=report_id,
            priority=priority,
            recipient_role="DISTRICT_OFFICER"
        )

    except Exception as error:

        print(
            "Surveillance notification error:",
            error
        )

    return jsonify({

        "success":
            True,

        "message":
            "Laboratory case sent to surveillance.",

        "laboratory":
            laboratory

    }), 200


# ============================================================
# MODULE STATUS
# ============================================================

@laboratory_bp.route(
    "/status",
    methods=["GET"]
)
@jwt_required()
def laboratory_status():

    ensure_laboratory_table()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM laboratory_records
            """
        )

        row = cursor.fetchone()

        total_records = int(
            row[0] or 0
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM laboratory_records
            WHERE sent_to_surveillance = 1
            """
        )

        row = cursor.fetchone()

        surveillance_records = int(
            row[0] or 0
        )

    finally:

        connection.close()

    return jsonify({

        "success":
            True,

        "module":
            "Laboratory Validation",

        "status":
            "active",

        "totalRecords":
            total_records,

        "sentToSurveillance":
            surveillance_records

    }), 200