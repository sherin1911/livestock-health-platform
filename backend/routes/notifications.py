from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from backend.services.notification_service import (
    get_user_notifications,
    get_unread_count,
    mark_notification_read,
    mark_all_read,
)
from backend.utils.authorization import get_current_identity


notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/api/notifications",
)


# ============================================================
# CURRENT USER HELPER
# ============================================================

def get_current_username():
    identity = get_current_identity()

    if not identity:
        return None

    return identity.get("username")


# ============================================================
# ALL NOTIFICATIONS
# ============================================================

@notifications_bp.route("", methods=["GET"])
@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def notifications():
    username = get_current_username()

    if not username:
        return jsonify(
            {
                "success": False,
                "message": "Unable to identify the current user.",
            }
        ), 401

    try:
        unread_only = request.args.get(
            "unread",
            default="false",
        ).lower() == "true"

        limit = request.args.get(
            "limit",
            default=50,
            type=int,
        )

        if limit < 1:
            limit = 50

        if limit > 200:
            limit = 200

        notification_list = get_user_notifications(
            username=username,
            unread_only=unread_only,
            limit=limit,
        )

        return jsonify(
            {
                "success": True,
                "notifications": notification_list,
                "count": len(notification_list),
                "unreadOnly": unread_only,
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load notifications.",
                "error": str(error),
            }
        ), 500


# ============================================================
# UNREAD NOTIFICATIONS
# ============================================================

@notifications_bp.route("/unread", methods=["GET"])
@jwt_required()
def unread_notifications():
    username = get_current_username()

    if not username:
        return jsonify(
            {
                "success": False,
                "message": "Unable to identify the current user.",
            }
        ), 401

    try:
        limit = request.args.get(
            "limit",
            default=50,
            type=int,
        )

        if limit < 1:
            limit = 50

        if limit > 200:
            limit = 200

        notification_list = get_user_notifications(
            username=username,
            unread_only=True,
            limit=limit,
        )

        return jsonify(
            {
                "success": True,
                "notifications": notification_list,
                "count": len(notification_list),
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load unread notifications.",
                "error": str(error),
            }
        ), 500


# ============================================================
# UNREAD COUNT
# ============================================================

@notifications_bp.route("/unread-count", methods=["GET"])
@jwt_required()
def unread_count():
    username = get_current_username()

    if not username:
        return jsonify(
            {
                "success": False,
                "message": "Unable to identify the current user.",
            }
        ), 401

    try:
        count = get_unread_count(username)

        return jsonify(
            {
                "success": True,
                "count": count,
                "unreadCount": count,
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to load unread notification count.",
                "error": str(error),
            }
        ), 500


# ============================================================
# MARK ONE NOTIFICATION AS READ
# ============================================================

@notifications_bp.route("/<int:notification_id>/read", methods=["PUT"])
@notifications_bp.route("/<int:notification_id>/read", methods=["PATCH"])
@jwt_required()
def mark_read(notification_id):
    username = get_current_username()

    if not username:
        return jsonify(
            {
                "success": False,
                "message": "Unable to identify the current user.",
            }
        ), 401

    try:
        result = mark_notification_read(
            username=username,
            notification_id=notification_id,
        )

        if result is False:
            return jsonify(
                {
                    "success": False,
                    "message": "Notification not found or already unavailable.",
                }
            ), 404

        return jsonify(
            {
                "success": True,
                "message": "Notification marked as read.",
                "notificationId": notification_id,
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to mark notification as read.",
                "error": str(error),
            }
        ), 500


# ============================================================
# MARK ALL NOTIFICATIONS AS READ
# ============================================================

@notifications_bp.route("/read-all", methods=["PUT"])
@notifications_bp.route("/read-all", methods=["PATCH"])
@jwt_required()
def mark_all_notifications_read():
    username = get_current_username()

    if not username:
        return jsonify(
            {
                "success": False,
                "message": "Unable to identify the current user.",
            }
        ), 401

    try:
        result = mark_all_read(username)

        if result is None:
            updated_count = 0
        elif isinstance(result, int):
            updated_count = result
        else:
            updated_count = 0

        return jsonify(
            {
                "success": True,
                "message": "All notifications marked as read.",
                "updatedCount": updated_count,
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Unable to mark all notifications as read.",
                "error": str(error),
            }
        ), 500


# ============================================================
# NOTIFICATION STATUS
# ============================================================

@notifications_bp.route("/status", methods=["GET"])
@jwt_required()
def notification_status():
    username = get_current_username()

    if not username:
        return jsonify(
            {
                "success": False,
                "message": "Unable to identify the current user.",
            }
        ), 401

    try:
        count = get_unread_count(username)

        return jsonify(
            {
                "success": True,
                "status": "operational",
                "unreadCount": count,
                "notificationSystem": True,
            }
        ), 200

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "status": "degraded",
                "notificationSystem": False,
                "message": "Notification service is currently unavailable.",
                "error": str(error),
            }
        ), 500
