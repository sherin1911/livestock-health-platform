from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from services.cluster_engine import (
    get_cluster_overview,
    build_location_clusters,
    build_symptom_clusters,
)
from utils.authorization import role_required


clusters_bp = Blueprint(
    "clusters",
    __name__,
    url_prefix="/api/clusters",
)


GOVERNMENT_ROLES = (
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN",
)


# ============================================================
# CLUSTER OVERVIEW
# ============================================================

@clusters_bp.route("/overview", methods=["GET"])
@jwt_required()
@role_required(*GOVERNMENT_ROLES)
def cluster_overview():
    try:
        days = request.args.get("days", default=14, type=int)

        if days < 1:
            days = 14

        if days > 90:
            days = 90

        overview = get_cluster_overview(days=days)

        return jsonify(
            {
                "success": True,
                "days": days,
                "data": overview,
                "message": (
                    "Cluster intelligence represents surveillance signals "
                    "for veterinary and government review. It is not an "
                    "outbreak declaration or autonomous diagnosis."
                ),
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load cluster overview.",
                "error": str(error),
            }
        ), 500


# ============================================================
# LOCATION CLUSTERS
# ============================================================

@clusters_bp.route("/locations", methods=["GET"])
@jwt_required()
@role_required(*GOVERNMENT_ROLES)
def location_clusters():
    try:
        days = request.args.get("days", default=14, type=int)

        if days < 1:
            days = 14

        if days > 90:
            days = 90

        clusters = build_location_clusters(days=days)

        return jsonify(
            {
                "success": True,
                "days": days,
                "clusters": clusters,
                "count": len(clusters),
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load location clusters.",
                "error": str(error),
            }
        ), 500


# ============================================================
# SYMPTOM CLUSTERS
# ============================================================

@clusters_bp.route("/symptoms", methods=["GET"])
@jwt_required()
@role_required(*GOVERNMENT_ROLES)
def symptom_clusters():
    try:
        days = request.args.get("days", default=14, type=int)

        if days < 1:
            days = 14

        if days > 90:
            days = 90

        clusters = build_symptom_clusters(days=days)

        return jsonify(
            {
                "success": True,
                "days": days,
                "clusters": clusters,
                "count": len(clusters),
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load symptom clusters.",
                "error": str(error),
            }
        ), 500


# ============================================================
# SINGLE LOCATION
# ============================================================

@clusters_bp.route("/location/<path:location>", methods=["GET"])
@jwt_required()
@role_required(*GOVERNMENT_ROLES)
def single_location_cluster(location):
    try:
        days = request.args.get("days", default=14, type=int)

        if days < 1:
            days = 14

        if days > 90:
            days = 90

        clusters = build_location_clusters(days=days)

        normalized_location = location.strip().lower()

        matched_cluster = None

        for cluster in clusters:
            cluster_location = str(
                cluster.get("location", "")
            ).strip().lower()

            if cluster_location == normalized_location:
                matched_cluster = cluster
                break

        if matched_cluster is None:
            return jsonify(
                {
                    "success": False,
                    "message": "No cluster information found for this location.",
                    "location": location,
                    "days": days,
                }
            ), 404

        return jsonify(
            {
                "success": True,
                "location": location,
                "days": days,
                "cluster": matched_cluster,
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load location cluster.",
                "error": str(error),
            }
        ), 500


# ============================================================
# CLUSTER STATUS
# ============================================================

@clusters_bp.route("/status", methods=["GET"])
@jwt_required()
@role_required(*GOVERNMENT_ROLES)
def cluster_status():
    try:
        days = request.args.get("days", default=14, type=int)

        if days < 1:
            days = 14

        if days > 90:
            days = 90

        overview = get_cluster_overview(days=days)

        location_clusters_data = overview.get(
            "locationClusters",
            overview.get("locations", []),
        )

        symptom_clusters_data = overview.get(
            "symptomClusters",
            overview.get("symptoms", []),
        )

        potential_clusters = 0
        high_priority_clusters = 0
        moderate_priority_clusters = 0
        watch_clusters = 0

        for cluster in location_clusters_data:
            if cluster.get("potentialEmergingCluster") is True:
                potential_clusters += 1

            priority = str(
                cluster.get("priority", "")
            ).upper()

            if priority == "HIGH PRIORITY":
                high_priority_clusters += 1

            elif priority == "MODERATE PRIORITY":
                moderate_priority_clusters += 1

            elif priority == "WATCH":
                watch_clusters += 1

        return jsonify(
            {
                "success": True,
                "status": "operational",
                "days": days,
                "summary": {
                    "locationClusters": len(location_clusters_data),
                    "symptomClusters": len(symptom_clusters_data),
                    "potentialEmergingClusters": potential_clusters,
                    "highPriorityClusters": high_priority_clusters,
                    "moderatePriorityClusters": moderate_priority_clusters,
                    "watchClusters": watch_clusters,
                },
                "interpretation": (
                    "Cluster scores are early-warning surveillance signals "
                    "based on reported cases, repeated symptoms, recency, "
                    "risk concentration and location patterns. Veterinary, "
                    "laboratory and epidemiological validation is required "
                    "before confirming a disease outbreak."
                ),
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "status": "degraded",
                "message": "Unable to calculate cluster status.",
                "error": str(error),
            }
        ), 500