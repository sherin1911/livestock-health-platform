import os
import sqlite3
from collections import Counter
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


# ============================================================
# HELPERS
# ============================================================

def table_exists(connection, table_name):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        """,
        (table_name,)
    )

    return cursor.fetchone() is not None


def normalize_location(location):
    if not location:
        return "Unknown"

    value = str(location).strip()

    if not value:
        return "Unknown"

    return value


def normalize_text(value):
    if not value:
        return ""

    return str(value).strip().lower()


def extract_symptoms(symptoms_text):
    """
    Converts a symptom string into individual symptom tokens.

    Examples:
        "fever, weakness, reduced appetite"
        "fever; weakness"
        "fever weakness"

    This is intentionally simple and suitable for the prototype.
    """

    if not symptoms_text:
        return []

    raw = str(symptoms_text)

    separators = [
        ",",
        ";",
        "|",
        "/"
    ]

    for separator in separators:
        raw = raw.replace(
            separator,
            ","
        )

    parts = []

    for item in raw.split(","):
        cleaned = item.strip().lower()

        if cleaned:
            parts.append(cleaned)

    return parts


def parse_date(value):
    if not value:
        return None

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d-%m-%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(
                str(value),
                fmt
            )
        except ValueError:
            continue

    return None


def risk_weight(risk_level):
    risk = normalize_text(
        risk_level
    ).upper()

    if risk == "HIGH":
        return 3

    if risk == "MEDIUM":
        return 2

    if risk == "LOW":
        return 1

    return 0


# ============================================================
# CLUSTER SCORING
# ============================================================

def calculate_cluster_score(
    report_count,
    high_risk_count,
    medium_risk_count,
    common_symptom_count,
    recent_report_count
):
    """
    Prototype cluster score.

    This score is an intelligence signal, not a disease diagnosis.

    Components:
        - Number of reports
        - Number of high-risk reports
        - Number of medium-risk reports
        - Repeated symptom pattern
        - Recent activity
    """

    score = 0

    # Report volume
    if report_count >= 2:
        score += 20

    if report_count >= 4:
        score += 15

    if report_count >= 7:
        score += 10

    # Risk concentration
    score += min(
        high_risk_count * 8,
        24
    )

    score += min(
        medium_risk_count * 4,
        12
    )

    # Repeated symptom signal
    if common_symptom_count >= 2:
        score += 8

    if common_symptom_count >= 3:
        score += 8

    # Recent activity
    if recent_report_count >= 2:
        score += 8

    if recent_report_count >= 4:
        score += 5

    return min(
        score,
        100
    )


def classify_cluster(score):
    """
    Classification is deliberately framed as surveillance intelligence.
    """

    if score >= 70:
        return "HIGH PRIORITY"

    if score >= 45:
        return "MODERATE PRIORITY"

    if score >= 25:
        return "WATCH"

    return "LOW SIGNAL"


# ============================================================
# BUILD LOCATION CLUSTERS
# ============================================================

def build_location_clusters(
    days=14,
    minimum_reports=2
):
    connection = get_connection()

    try:
        if not table_exists(
            connection,
            "health_reports"
        ):
            return []

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                report_id,
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
                status,
                created_at
            FROM health_reports
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        now = datetime.now()

        cutoff = now - timedelta(
            days=days
        )

        location_groups = {}

        for row in rows:

            created_at = parse_date(
                row["created_at"]
            )

            # Ignore records that are too old
            # when a valid date is available.
            if created_at and created_at < cutoff:
                continue

            location = normalize_location(
                row["location"]
            )

            if location not in location_groups:
                location_groups[location] = []

            location_groups[location].append(
                dict(row)
            )

        clusters = []

        for location, reports in location_groups.items():

            if len(reports) < minimum_reports:
                continue

            high_risk_count = sum(
                1
                for report in reports
                if normalize_text(
                    report.get("risk_level")
                ).upper() == "HIGH"
            )

            medium_risk_count = sum(
                1
                for report in reports
                if normalize_text(
                    report.get("risk_level")
                ).upper() == "MEDIUM"
            )

            low_risk_count = sum(
                1
                for report in reports
                if normalize_text(
                    report.get("risk_level")
                ).upper() == "LOW"
            )

            # ------------------------------------------------
            # SYMPTOM FREQUENCY
            # ------------------------------------------------

            symptom_counter = Counter()

            for report in reports:

                symptoms = extract_symptoms(
                    report.get("symptoms")
                )

                for symptom in symptoms:
                    symptom_counter[symptom] += 1

            repeated_symptoms = [
                {
                    "symptom": symptom,
                    "count": count
                }
                for symptom, count
                in symptom_counter.most_common()
                if count >= 2
            ]

            common_symptom_count = len(
                repeated_symptoms
            )

            # ------------------------------------------------
            # RECENT REPORT COUNT
            # ------------------------------------------------

            recent_cutoff = now - timedelta(
                days=3
            )

            recent_report_count = 0

            for report in reports:

                created_at = parse_date(
                    report.get("created_at")
                )

                if (
                    created_at
                    and created_at >= recent_cutoff
                ):
                    recent_report_count += 1

            # If timestamps are unavailable,
            # use report volume as a fallback.
            if recent_report_count == 0:
                recent_report_count = min(
                    len(reports),
                    4
                )

            # ------------------------------------------------
            # SPECIES DISTRIBUTION
            # ------------------------------------------------

            species_counter = Counter()

            for report in reports:

                species = report.get(
                    "species"
                )

                if species:
                    species_counter[
                        str(species).strip()
                    ] += 1

            species_distribution = [
                {
                    "species": species,
                    "count": count
                }
                for species, count
                in species_counter.most_common()
            ]

            # ------------------------------------------------
            # SCORE
            # ------------------------------------------------

            score = calculate_cluster_score(
                report_count=len(reports),
                high_risk_count=high_risk_count,
                medium_risk_count=medium_risk_count,
                common_symptom_count=common_symptom_count,
                recent_report_count=recent_report_count
            )

            priority = classify_cluster(
                score
            )

            # ------------------------------------------------
            # COORDINATES
            # ------------------------------------------------

            latitude = None
            longitude = None

            for report in reports:
                if (
                    report.get("latitude") is not None
                    and report.get("longitude") is not None
                ):
                    latitude = report.get(
                        "latitude"
                    )

                    longitude = report.get(
                        "longitude"
                    )

                    break

            # ------------------------------------------------
            # CLUSTER INTERPRETATION
            # ------------------------------------------------

            signal_reasons = []

            if len(reports) >= 4:
                signal_reasons.append(
                    "Multiple reports from the same location"
                )

            if high_risk_count >= 1:
                signal_reasons.append(
                    "High-risk reports are present"
                )

            if common_symptom_count >= 1:
                signal_reasons.append(
                    "Repeated symptom pattern detected"
                )

            if recent_report_count >= 2:
                signal_reasons.append(
                    "Recent reporting activity detected"
                )

            # Explicit wording to avoid autonomous diagnosis.
            emerging_signal = (
                score >= 45
            )

            clusters.append(
                {
                    "location": location,

                    "clusterScore": score,

                    "priority": priority,

                    "potentialEmergingCluster":
                        emerging_signal,

                    "reportCount":
                        len(reports),

                    "highRiskCount":
                        high_risk_count,

                    "mediumRiskCount":
                        medium_risk_count,

                    "lowRiskCount":
                        low_risk_count,

                    "recentReportCount":
                        recent_report_count,

                    "repeatedSymptoms":
                        repeated_symptoms,

                    "speciesDistribution":
                        species_distribution,

                    "latitude":
                        latitude,

                    "longitude":
                        longitude,

                    "signalReasons":
                        signal_reasons,

                    "reportIds": [
                        report.get("report_id")
                        for report in reports
                    ]
                }
            )

        # ----------------------------------------------------
        # PRIORITY SORTING
        # ----------------------------------------------------

        clusters.sort(
            key=lambda item: (
                item["clusterScore"],
                item["highRiskCount"],
                item["reportCount"]
            ),
            reverse=True
        )

        return clusters

    finally:
        connection.close()


# ============================================================
# SYMPTOM CLUSTERS
# ============================================================

def build_symptom_clusters(
    days=14,
    minimum_occurrences=2
):
    connection = get_connection()

    try:
        if not table_exists(
            connection,
            "health_reports"
        ):
            return []

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                report_id,
                species,
                symptoms,
                location,
                risk_level,
                risk_score,
                created_at
            FROM health_reports
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        cutoff = datetime.now() - timedelta(
            days=days
        )

        symptom_map = {}

        for row in rows:

            created_at = parse_date(
                row["created_at"]
            )

            if (
                created_at
                and created_at < cutoff
            ):
                continue

            symptoms = extract_symptoms(
                row["symptoms"]
            )

            for symptom in symptoms:

                if symptom not in symptom_map:
                    symptom_map[symptom] = []

                symptom_map[symptom].append(
                    dict(row)
                )

        results = []

        for symptom, reports in symptom_map.items():

            if len(reports) < minimum_occurrences:
                continue

            location_counter = Counter(
                normalize_location(
                    report.get("location")
                )
                for report in reports
            )

            species_counter = Counter(
                str(
                    report.get("species")
                    or "Unknown"
                )
                for report in reports
            )

            high_risk = sum(
                1
                for report in reports
                if normalize_text(
                    report.get("risk_level")
                ).upper() == "HIGH"
            )

            average_risk = 0

            scores = [
                float(
                    report.get("risk_score")
                    or 0
                )
                for report in reports
            ]

            if scores:
                average_risk = round(
                    sum(scores) / len(scores),
                    1
                )

            results.append(
                {
                    "symptom":
                        symptom,

                    "occurrenceCount":
                        len(reports),

                    "highRiskCount":
                        high_risk,

                    "averageRiskScore":
                        average_risk,

                    "topLocations": [
                        {
                            "location": location,
                            "count": count
                        }
                        for location, count
                        in location_counter.most_common(5)
                    ],

                    "species": [
                        {
                            "species": species,
                            "count": count
                        }
                        for species, count
                        in species_counter.most_common()
                    ],

                    "reportIds": [
                        report.get("report_id")
                        for report in reports
                    ]
                }
            )

        results.sort(
            key=lambda item: (
                item["occurrenceCount"],
                item["highRiskCount"],
                item["averageRiskScore"]
            ),
            reverse=True
        )

        return results

    finally:
        connection.close()


# ============================================================
# COMPLETE CLUSTER OVERVIEW
# ============================================================

def get_cluster_overview(
    days=14
):
    location_clusters = build_location_clusters(
        days=days
    )

    symptom_clusters = build_symptom_clusters(
        days=days
    )

    potential_clusters = [
        cluster
        for cluster in location_clusters
        if cluster[
            "potentialEmergingCluster"
        ]
    ]

    high_priority_clusters = [
        cluster
        for cluster in location_clusters
        if cluster[
            "priority"
        ] == "HIGH PRIORITY"
    ]

    total_cluster_reports = sum(
        cluster["reportCount"]
        for cluster in location_clusters
    )

    return {
        "success": True,

        "analysisWindowDays": days,

        "summary": {
            "locationsAnalysed":
                len(location_clusters),

            "potentialEmergingClusters":
                len(potential_clusters),

            "highPriorityClusters":
                len(high_priority_clusters),

            "reportsIncluded":
                total_cluster_reports,

            "repeatedSymptomSignals":
                len(symptom_clusters)
        },

        "clusters":
            location_clusters,

        "symptomClusters":
            symptom_clusters,

        "notice":
            "Cluster results are surveillance intelligence signals for veterinary and epidemiological review. They do not constitute autonomous disease diagnosis or confirmed outbreak declarations."
    }


# ============================================================
# SINGLE LOCATION ANALYSIS
# ============================================================

def analyze_location(
    location,
    days=14
):
    location = normalize_location(
        location
    )

    clusters = build_location_clusters(
        days=days,
        minimum_reports=1
    )

    for cluster in clusters:

        if normalize_text(
            cluster["location"]
        ) == normalize_text(location):

            return {
                "success": True,
                "cluster": cluster
            }

    return {
        "success": True,
        "cluster": None
    }